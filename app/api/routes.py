from fastapi import APIRouter, Response, Request

from langgraph.graph.state import CompiledStateGraph

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
    state: State = {"input": question.question, "output": str(), "tools_output": None}
    context: Context = {"uuid": question.session_id, "max_result": 50}
    graph: CompiledStateGraph = request.app.state.graph
    result = await graph.ainvoke(state, context=context)
    return result
    # agent_rooter.state.last_request_per_user[session_id] = int(time.time())
    # try:
    #    sql_result = await run_in_threadpool(
    #        lambda: agent_rooter.state.sql_agent.get_response_with_memory(
    #            session_id, user_question
    #        )
    #    )
    #    queries = verify_and_extract_sql_query(sql_result.content, max_result_limit)
    #    data = await run_in_threadpool(
    #        lambda: execute_queries(agent_rooter.state.sql_agent.get_engine(), queries)
    #    )
    #    if is_empty_result(data):
    #        data = {"result": "no matching item"}


#
#    final_response = await run_in_threadpool(
#        lambda: agent_rooter.state.nlp_agent.get_response_with_memory(
#            session_id=session_id,
#            user_question=user_question,
#            dynamic_variables={
#                "query": queries,
#                "data": str(data),
#                "result_limit": max_result_limit,
#            },
#        )
#    )
#    agent_rooter.state.sql_agent.get_memory().rotate_history(
#        session_id, max_questions=3
#    )
#    agent_rooter.state.nlp_agent.get_memory().rotate_history(
#        session_id, max_questions=3
#    )
#    return {
#        "status": "success",
#        "response": str(final_response.content),
#    }
#
# except Exception as e:
#    logging.exception("Error processing request for session %s: %s", session_id, e)
#    try:
#        error_response = await run_in_threadpool(
#            lambda: agent_rooter.state.nlp_agent.get_response_with_memory(
#                session_id=session_id,
#                user_question=user_question,
#                dynamic_variables={
#                    "query": queries
#                    if "queries" in locals()
#                    else ["No query generated"],
#                    "data": str(e),
#                    "result_limit": max_result_limit,
#                },
#            )
#        )
#        response.status_code = 200
#        return {
#            "status": "success",
#            "response": str(error_response.content),
#        }
#    except Exception as nlp_error:
#        logging.exception("NLP agent error after SQL failure: %s", nlp_error)
#        response.status_code = 500
#        return {
#            "status": "error",
#            "response": "Internal server error. Please retry later.",
#        }
