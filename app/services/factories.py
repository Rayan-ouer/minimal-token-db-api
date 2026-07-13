import os
import toml
from langgraph.graph import StateGraph
from langchain_core.prompts import BasePromptTemplate

from app.services.agent import Agent
from app.services.ai_providers import PROVIDERS


def filter_none_values(data: dict) -> dict:
    cleaned = {}
    for key, value in data.items():
        if value is not None:
            cleaned[key] = value
    return cleaned


def init_ai_agent(prompt_settings: BasePromptTemplate = None) -> Agent:
    provider_name = os.getenv("AI_PROVIDER", "").lower()
    model_name = os.getenv("AI_MODEL")

    if provider_name not in PROVIDERS:
        raise ValueError(
            f"Unknown AI provider, You can add provider in ai_providers.py '{provider_name}'. "
            f"Valid providers are: {', '.join(PROVIDERS.keys())}"
        )

    config = PROVIDERS[provider_name]
    provider_class = config["class"]
    key_name = config["key"]

    api_key = os.getenv(key_name) if key_name else None
    if key_name and not api_key:
        raise RuntimeError(
            f"Missing API key for provider '{provider_name}'. "
            f"Expected environment variable '{key_name}', but it was not found."
        )

    model_args = {"model": model_name, **model_config}
    if api_key:
        model_args["api_key"] = api_key

    model = provider_class(**filter_none_values(model_args))
    agent = IAModel()
    agent.set_engine(engine)
    agent.set_model(model)
    agent.set_prompt(prompt_settings)

    return agent

class AgentFactory:
    def __init__(self):
        pass

    def create_workflows(self, file: str) -> StateGraph:
        config: dict = toml.load(file)["pipeline"]

        for pipeline in config:
            agent = pipeline["pipeline.agent"]
            for agent in pipeline:
                name: str = agent["name"]
                provider: str = agent["provider"]
                