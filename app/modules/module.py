from abc import ABC, abstractmethod


class Module(ABC):
    """Interface for module."""

    @abstractmethod
    def run(self) -> None:
        pass
