from typing_extensions import TypedDict, Any


class Context(TypedDict):
    uuid: str
    db_conn: str
