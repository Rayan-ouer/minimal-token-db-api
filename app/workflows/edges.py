from abc import ABC, abstractmethod
from langgraph.graph import StateGraph
from langgraph.graph import START, END

from app.workflows.routes import ROUTERS


def resolve_node(name):
    if name == "START":
        return START
    if name == "END":
        return END
    return name


class Edge(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def build(self, graph: StateGraph):
        pass


class NormalEdge(Edge):
    def build(self, graph: StateGraph):
        graph.add_edge(
            resolve_node(self.config["source"]), resolve_node(self.config["dest"])
        )


class ConditionalEdge(Edge):
    def build(self, graph: StateGraph):
        graph.add_conditional_edges(
            resolve_node(self.config["source"]),
            ROUTERS[self.config["router"]],
            resolve_node(self.config["routes"]),
        )
