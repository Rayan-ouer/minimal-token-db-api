from app.schemas import Context, State
from typing import Callable, Any


def redirection(state: State) -> str:
    return state["decision"]


ROUTERS: dict[str, Callable[["State", "Context"], Any]] = {
    "redirection": redirection,
}
