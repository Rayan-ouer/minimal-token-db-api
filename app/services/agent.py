from langchain_core.prompts import BasePromptTemplate
from typing import Optional, Dict, Any
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import AIMessage


class IAModel:
    def __init__(self):
        self._model: Optional[BaseLanguageModel] = None
        self._prompt: Optional[BasePromptTemplate] = None
        self._engine = None
        self._memory = ChatMemory()

    def set_model(self, model: BaseLanguageModel):
        self._model = model

    def set_prompt(self, prompt: BasePromptTemplate):
        self._prompt = prompt

    def set_engine(self, engine):
        self._engine = engine

    def get_engine(self):
        return self._engine

    def get_memory(self):
        return self._memory

    def get_response(self, variables: Dict[str, Any]):
        if not self._model or not self._prompt:
            raise RuntimeError(
                "The template and prompt must be defined before generating a response."
            )

        chain = self._prompt | self._model
        return chain.invoke(variables)

    def get_response_with_memory(
        self,
        session_id: int,
        user_question: Optional[str] = None,
        add_to_history: bool = True,
        dynamic_variables: Optional[Dict[str, Any]] = None,
        **invoke_kwargs,
    ) -> AIMessage:

        if user_question is not None and add_to_history:
            self._memory.add_user_message(session_id, user_question)

        history = self._memory.get_session_by_id(session_id)
        prompt_copy = self._prompt.model_copy()
        print(f"History : {history}")
        for message in history.messages:
            prompt_copy.messages.append(message)

        chain = prompt_copy | self._model
        result = chain.invoke(dynamic_variables or {}, **invoke_kwargs)

        if add_to_history:
            self._memory.add_ai_message(session_id, result.content)

        return result
