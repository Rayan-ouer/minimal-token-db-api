import re
import os
from typing import Optional, Any

import sqlparse
from sqlalchemy import inspect
from urllib.parse import quote_plus
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine


from module import Module
from app.utils import extract_between


class Database(Module):
    def __init__(self):
        self._engine: Engine = create_engine(
            self.get_database_url(),
            pool_pre_ping=True,
            pool_recycle=28800,
            echo=False,
        )
        self.introspect_schema()

    def get_engine(self) -> Engine:
        return self._engine

    def get_database_url() -> str:
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
    
    def extract_sql_query(self, query: str, max_limit: Optional[int]) -> Optional[list[str]]:
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
    
    def run(self):
        return super().run()

