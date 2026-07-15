from abc import ABC, abstractmethod
from app.schemas.state import State
from app.schemas.context import Context


class Module(ABC):
    """Interface for module."""

    @abstractmethod
    def run(self, state: State, context: Context):
        pass

    @abstractmethod
    def get_context(self) -> dict[str, str]:
        pass
