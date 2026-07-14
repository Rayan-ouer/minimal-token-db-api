import toml
import sys

from app.schemas.agent_data import AgentData

from app.agents.agent import Agent
from app.agents.factory import AgentFactory
from app.prompt import PROMPTS
from app.prompt.prompts import init_prompt



class AgentRegistry:
    _agents: dict[str, Agent] = {}

    def __init__(self, file: str):
        self.register(file)
    
    def set_agent(self, name: str, agent: Agent):
        self._agents[name] = agent

    def register(self, file: str):
        try:
            config: dict = toml.load(file)["pipeline"]
        except OSError as e:
            print(f"File error: {e}", file=sys.stderr)
            return None

        for pipeline in config:
            print(f"{pipeline=}")
            agent_data = pipeline["agents"]
            agents = agent_data if isinstance(agent_data, list) else [agent_data]
            for agent in agents:
                data: AgentData = AgentData(
                    agent["model"],
                    agent["provider"],
                    agent["settings"],
                    init_prompt(PROMPTS[agent["prompt"]]),
                    AgentFactory().get_modules(agent["modules"]),
                )
                self.set_agent(agent["name"], AgentFactory().create_agent(data))

    def get_agent(self, name: str) -> Agent:
        return self._agents[name]
    
    def get_register(self) -> dict[str, Agent]:
        return self._agents
    



