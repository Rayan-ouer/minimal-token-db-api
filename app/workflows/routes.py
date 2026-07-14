from app.schemas import Context, State
from typing import Callable, Any


def redirection(state: State) -> str:
    if state["tools_output"] == "Fail":
        return "exception"
    return "explainer"


ROUTERS: dict[str, Callable[["State", "Context"], Any]] = {
    "redirection": redirection,
}
