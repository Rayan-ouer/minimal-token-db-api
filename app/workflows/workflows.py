import sys
import toml
from langgraph.graph import StateGraph

from app.agents.factory import AgentFactory
from app.agents.register import AgentRegistry


class Workflows:
    _workflows: StateGraph
    _config: str

    def __init__(self, config: str):
        self._config = config
    
    def create(self, register: AgentRegistry):
        for name, agent in register.get_register().items():
            self._workflows.add_node(name, agent.get_response_with_memory())
        
        try:
            config: dict = toml.load(config)["edge"]
        except OSError as e:
            print(f"File error: {e}", file=sys.stderr)
            return None
        for edge in config:
            

