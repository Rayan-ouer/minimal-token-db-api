import os
import logging
from dotenv import load_dotenv


from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.agents.register import AgentRegistry
from app.workflows.workflows import Workflows
from app.api.routes import agent_rooter

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Startup...")
    register: AgentRegistry = AgentRegistry(os.getenv("CONFIGURATION"))
    workflows: Workflows = Workflows(os.getenv("CONFIGURATION"))
    workflows.create(register)
    app.state.graph = workflows.get_graph()
    app.state.registry = register
    print(app.state.graph.get_graph().draw_ascii())
    yield
    logging.info("Shutting down...")


app = FastAPI(
    title="efficient token workflow engine API",
    description="An API for building multi-agent AI workflows with optimized token usage.",
    version="0.1",
    lifespan=lifespan,
)

app.include_router(agent_rooter)
