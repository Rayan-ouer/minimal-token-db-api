import os
import logging
from dotenv import load_dotenv

from IPython.display import display, Image

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
    chat_graph = workflows.create(register)
    print(chat_graph.get_graph().draw_ascii())
    yield
    logging.info("Shutting down...")
    # when shutting down


app = FastAPI(
    title="minimum ai token consumption api",
    description="An API that allows the AI ​​to consume as few tokens as possible.",
    version="0.1",
    lifespan=lifespan,
)

app.include_router(agent_rooter)
