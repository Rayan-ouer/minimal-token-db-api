import re
import os
from typing import Optional, Any

import sqlparse
from sqlalchemy import inspect, text
from urllib.parse import quote_plus
from sqlalchemy.engine import Engine, CursorResult
from sqlalchemy import create_engine

from app.modules import Module
from app.schemas.state import State
from app.schemas.context import Context
from app.utils.strings import extract_between


class Database(Module):
    def __init__(self):
        self._engine: Engine = create_engine(
            self.get_database_url(),
            pool_pre_ping=True,
            pool_recycle=28800,
            echo=False,
        )

    def get_engine(self) -> Engine:
        return self._engine

    def get_database_url(self) -> str:
        username: str = quote_plus(os.getenv("DB_USERNAME"))
        password: str = quote_plus(os.getenv("DB_PASSWORD"))

        return (
            f"mysql+pymysql://{username}:{password}"
            f"@{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DATABASE')}"
        )

    def set_limit(self, query: str, max_limit: Optional[int]) -> str:
        if not max_limit:
            return query.strip().rstrip(";") + ";"
        query = re.sub(r";\s*$", "", query)
        limit_match = re.search(r"\bLIMIT\s+(\d+)", query, re.IGNORECASE)
        if limit_match:
            existing_limit = int(limit_match.group(1))
            if existing_limit > max_limit:
                query = re.sub(
                    r"\bLIMIT\s+\d+", f"LIMIT {max_limit}", query, flags=re.IGNORECASE
                )
        else:
            query += f" LIMIT {max_limit}"
        return query.strip() + ";"

    def extract_sql_query(
        self, query: str, max_limit: int = 50) -> Optional[list[str]]:
        query: str = sqlparse.format(query, reindent=True, keyword_case="upper")
        clean_query: str = extract_between(query, "SELECT", ";")

        if not clean_query:
            return None
        queries = clean_query.split(";")
        return [self.set_limit(q.strip(), max_limit) for q in queries if q.strip()]

    def introspect_schema(self) -> dict[str, Any]:
        inspector = inspect(self._engine)
        schema: dict = {}

        print(f"{type(inspector)=}")
        for table_name in inspector.get_table_names():
            schema[table_name] = {
                "columns": {
                    column["name"]: str(column["type"])
                    for column in inspector.get_columns(table_name)
                },
            }
        return schema

    def extract_content(self, result: CursorResult, limit: int) -> list[dict[str, Any]]:

        rows = result.mappings().fetchmany(limit)

        if rows:
            return [dict(row) for row in rows]
        return [{"rows_affected": result.rowcount}]

    def execute_queries(self, queries: list[str], limit: int) -> list[str]:
        results = []

        if not queries:
            return results
        try:
            with self._engine.connect() as connection:
                for query in queries:
                    if not query or not query.strip():
                        continue
                    clean_query = query.strip().rstrip(";") + ";"
                    result = connection.execute(text(clean_query))

                    extracted_data = self.extract_content(result, limit)
                    results.append(extracted_data)
                return results
        except Exception as e:
            print(f"Error while executing queries: {e}")
            raise

    def get_context(self) -> dict[str, str]:
        return {"database_schema": self.introspect_schema()}

    def run(self, state: State, context: Context):
        queries: list[str] = self.extract_sql_query(state["output"], context["max_result"])
        print(f"{queries=}")
        results: list[str] = self.execute_queries(queries, context["max_result"])
        print(f"{results=}")
        if not results:
            state["decision"] = "exception"
            return
        state["tools_output"].update({"database": results})
        state["decision"] = "explainer"

