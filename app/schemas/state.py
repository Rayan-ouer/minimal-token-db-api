from typing_extensions import TypedDict, Any


class State(TypedDict):
    input: str
    output: str
    tools_output: Any
