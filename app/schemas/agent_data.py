from dataclasses import dataclass
from langchain_core.prompts import BasePromptTemplate
from app.modules.module import Module


@dataclass
class AgentData:
    model: str
    provider: str
    settings: dict
    prompt: BasePromptTemplate
    modules: list[Module]
