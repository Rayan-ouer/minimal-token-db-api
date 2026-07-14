import os

from app.agents.agent import Agent
from app.schemas.agent_data import AgentData
from app.modules import MODULES, Module
from app.agents.ai_providers import PROVIDERS


def filter_none_values(data: dict) -> dict:
    cleaned: dict = {}

    for key, value in data.items():
        if value:
            cleaned[key] = value
    return cleaned


class AgentFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_modules(modules: list[str]) -> list[Module]:
        mods: list[Module] = []

        for element in modules:
            mods.append(MODULES[element])
        return mods

    @staticmethod
    def create_agent(agentdata: AgentData) -> Agent:
        try:
            config = PROVIDERS[agentdata.provider]
        except:
             raise ValueError(
                f"Unknown AI provider, You can add provider in ai_providers.py '{agentdata.provider}'. "
                f"Valid providers are: {', '.join(PROVIDERS.keys())}"
            )
        provider_class = config["class"]
        key_name = config["key"]
        api_key = os.getenv(key_name) if key_name else None
        if key_name and not api_key:
            raise RuntimeError(
                f"Missing API key for provider '{agentdata.provider}'. "
                f"Expected environment variable '{key_name}', but it was not found."
            )
        for module in agentdata.modules:
            agentdata.prompt += module.get_context()
        model_args = {"model": agentdata.model, **agentdata.settings}
        if api_key:
            model_args["api_key"] = api_key

        model = provider_class(**filter_none_values(model_args))
        agent = Agent(model=model, prompt=agentdata.prompt, modules=agentdata.modules)
        return agent
