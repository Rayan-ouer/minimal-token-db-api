from fastapi import APIRouter, Response, Request

from langgraph.graph.state import CompiledStateGraph
from langchain_core.chat_history import InMemoryChatMessageHistory

from app.schemas import Question, State, Context


agent_rooter: APIRouter = APIRouter()


@agent_rooter.get("/")
def read_root():
    return {
        "title": "minimum ai token consumption api",
        "description": "An API that allows the AI ​​to consume as few tokens as possible.",
        "version": "0.1",
    }


@agent_rooter.get("/health")
def get_health():
    return {"status": "ok"}


@agent_rooter.post("/chat")
async def invoke_agent(question: Question, response: Response, request: Request):
    state: State = {"input": question.question, "output": None, "decision": None, "tools_output": {}, "messages": {question.session_id: InMemoryChatMessageHistory()}}
    context: Context = {"uuid": question.session_id, "max_result": 50}
    graph: CompiledStateGraph = request.app.state.graph
    result = await graph.ainvoke(state, context=context)
    return result
