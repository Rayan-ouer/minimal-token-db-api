import logging
from dotenv import load_dotenv

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import agent_rooter

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # at startup
    yield
    # when shutting down


app = FastAPI(
    title="minimum ai token consumption api",
    description="An API that allows the AI ​​to consume as few tokens as possible.",
    version="0.1",
)

app.include_router(agent_rooter)
