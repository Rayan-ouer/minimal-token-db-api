import os
from langchain_openai import ChatOpenAI 
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

PROVIDERS = {
    "openai": {
        "class": ChatOpenAI,
        "key": "OPENAI_API_KEY"
    },
    "groq": {
        "class": ChatGroq,
        "key": "GROQ_API_KEY"
    },
    "ollama": {
        "class": ChatOllama,
        "key": None
    },
}
