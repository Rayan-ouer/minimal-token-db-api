from app.schemas.state import State


def redirection(state: State) -> str:
    if state["tools_output"] == "Fail":
        return "exception"
    return "explainer"
