from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from typing import Optional
from langchain_core.language_models import BaseLanguageModel

PROVIDERS: dict[str, dict[BaseLanguageModel, Optional[str]]] = {
    "openai": {"class": ChatOpenAI, "key": "OPENAI_API_KEY"},
    "groq": {"class": ChatGroq, "key": "GROQ_API_KEY"},
    "ollama": {"class": ChatOllama, "key": None},
}
