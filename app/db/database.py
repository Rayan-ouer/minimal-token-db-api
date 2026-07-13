import os
import re
import sqlparse
from typing import Optional, Any
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, CursorResult

def extract_content(result: CursorResult) -> list[dict[str, Any]]:
    try:
        rows = result.fetchall()
        if rows:
            return [dict(row._asdict()) for row in rows]
        else:
            return [{"status": "success", "rows_affected": result.rowcount}]
    except Exception:
        return [{"status": "success", "rows_affected": result.rowcount}]


def execute_queries(engine: Engine, query_list: list[str]) -> list[str]:
    results = []

    if not query_list:
        return results
    try:
        with engine.connect() as connection:
            for query in query_list:
                if not query or not query.strip():
                    continue
                clean_query = query.strip().rstrip(";") + ";"
                result = connection.execute(text(clean_query))

                extracted_data = extract_content(result)
                results.append(extracted_data)

            return results

    except Exception as e:
        print(f"Erreur lors de l'exécution des requêtes: {e}")
        raise


def is_empty_result(data: list[str]) -> bool:
    if not isinstance(data, list) or len(data) != 1:
        return False
    row = data[0]
    return isinstance(row, dict) and row.get("rows_affected") == 0
