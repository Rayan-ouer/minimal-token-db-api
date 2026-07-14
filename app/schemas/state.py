from typing_extensions import TypedDict, Any
from langchain_core.messages import AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory


class State(TypedDict):
    input: str
    output: AIMessage | None
    decision: str | None
    tools_output: dict[str, Any]
    messages: dict[str, InMemoryChatMessageHistory]