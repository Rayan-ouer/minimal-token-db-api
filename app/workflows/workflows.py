import sys
import toml
from langgraph.graph import StateGraph

from app.schemas.state import State
from app.schemas.context import Context
from app.agents.factory import AgentFactory
from app.agents.register import AgentRegistry
from app.workflows import EDGE_TYPES
from app.workflows.edges import Edge


class Workflows:
    _workflows: StateGraph
    _config: str

    def __init__(self, config: str):
        self._config = config
        self._workflows: StateGraph = StateGraph(
            state_schema=State, context_schema=Context
        )

    def create(self, register: AgentRegistry):
        for name, agent in register.get_register().items():
            self._workflows.add_node(name, agent.run)

        try:
            self._config: dict = toml.load(self._config)["edge"]
        except OSError as e:
            print(f"File error: {e}", file=sys.stderr)
            return None
        for edge_config in self._config:
            edge: Edge = EDGE_TYPES[edge_config.get("type", "normal")](edge_config)
            edge.build(self._workflows)
        return self._workflows.compile()
