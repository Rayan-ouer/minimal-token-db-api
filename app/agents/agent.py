from typing import Optional, Dict, Any
from langgraph.runtime import Runtime
from langchain_core.messages import AIMessage
from langchain_core.prompts import BasePromptTemplate
from langchain_core.language_models import BaseLanguageModel

from app.schemas.state import State
from app.schemas.context import Context
from app.modules.module import Module


class Agent:
    def __init__(
        self,
        model: BaseLanguageModel,
        prompt: BasePromptTemplate,
        modules: list[Module] = None,
    ):
        self._model: Optional[BaseLanguageModel] = model
        self._prompt: Optional[BasePromptTemplate] = prompt
        self._modules: list[Module] = modules

    def set_model(self, model: BaseLanguageModel):
        self._model = model

    def set_prompt(self, prompt: BasePromptTemplate):
        self._prompt = prompt

    def get_response(self, variables: Dict[str, Any]) -> AIMessage:
        if not self._model or not self._prompt:
            raise RuntimeError(
                "The template and prompt must be defined before generating a response."
            )

        chain = self._prompt | self._model
        return chain.invoke(variables)

    def run(self, state: State, runtime: Runtime[Context]):
        variables = {
            "input": state["input"],
            "output": state["output"],
            "tools_output": state["tools_output"],
        }
        response: AIMessage = self.get_response(variables)
        state["output"] = response.content

        for module in self._modules:
            module.run(state=state, context=runtime.context)
        return state
