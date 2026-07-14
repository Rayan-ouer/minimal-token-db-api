from app.modules.module import Module
from app.schemas.state import State
from app.schemas.context import Context
from langchain_core.chat_history import InMemoryChatMessageHistory


class Memory(Module):
    def __init__(self):
        self._conversation: dict[int, InMemoryChatMessageHistory] = {}
        self._counter_question: dict[int, int] = {}

    def get_session_by_id(self, session_id: int) -> InMemoryChatMessageHistory:
        if session_id not in self._conversation:
            self._conversation[session_id] = InMemoryChatMessageHistory()
            self._counter_question[session_id] = 0
        return self._conversation[session_id]

    def clear_history_by_id(self, session_id: int):
        if session_id in self._conversation:
            self._conversation[session_id] = InMemoryChatMessageHistory()
        if session_id in self._counter_question:
            self._counter_question[session_id] = 0

    def clear_all_sessions(self):
        for session_id in self._conversation:
            self._conversation[session_id].clear()
        self._conversation = {}

    def get_session_callable(self, session_id: int):
        def get_history(session_id: str) -> InMemoryChatMessageHistory:
            return self.get_session_by_id(session_id)

        return get_history

    def add_user_message(self, session_id: int, user_message):
        history = self.get_session_by_id(session_id)
        self._counter_question[session_id] += 1
        history.add_user_message(user_message)

    def add_ai_message(self, session_id: int, ai_message):
        history = self.get_session_by_id(session_id)
        history.add_ai_message(ai_message)

    def reset_history(self, session_id: int, max_question: int):
        if session_id not in self._counter_question:
            return
        counter = self._counter_question[session_id]
        if counter >= max_question:
            self.clear_history_by_id(session_id)

    def rotate_history(self, session_id: int, max_questions: int):
        if session_id not in self._conversation:
            return
        history = self._conversation[session_id]
        total_messages = len(history.messages)
        max_messages = max_questions * 2
        if total_messages > max_messages:
            messages_to_keep = history.messages[-max_messages:]
            history.messages = messages_to_keep
            self._counter_question[session_id] = max_questions
    
    def get_context(self) -> dict[str, str]:
        return {"conversation": self._conversation}

    def run(self, state: State, context: Context):
        state["messages"].get(context["uuid"], context["uuid"]).add_user_message(state["input"])
