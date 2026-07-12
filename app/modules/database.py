import os
from sqlalchemy import inspect
from typing import Any
from urllib.parse import quote_plus
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine



class Database:
    def __init__(self):
        self._engine: Engine = create_engine(
            self.get_database_url(),
            pool_pre_ping=True,
            pool_recycle=28800,
            echo=False,
        )

    def get_engine(self) -> Engine:
        return self._engine

    def get_database_url() -> str:
        username: str = quote_plus(os.getenv("AI_USERNAME"))
        password: str = quote_plus(os.getenv("AI_PASSWORD"))

        return (
            f"mysql+pymysql://{username}:{password}"
            f"@{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DATABASE')}"
        )

    def introspect_schema(self) -> dict[str, Any]:
        inspector = inspect(self._engine)
        schema: dict = {}

        print(f"{type(inspector)=}")
        for table_name in inspector.get_table_names():
            schema[table_name] = {
                "columns": {
                    c["name"]: str(c["type"]) for c in inspector.get_columns(table_name)
                },
            }
        return schema
