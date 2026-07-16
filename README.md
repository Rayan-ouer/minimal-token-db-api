# Efficient token workflow engine API

Efficient token workflow engine is an extensible framework for building configurable multi-agent AI workflows.

It allows you to:

- Define workflows declaratively using TOML.
- Compose AI agents with reusable capability modules.
- Support multiple LLM providers.
- Build conditional execution graphs with LangGraph.
- Optimize token usage by routing tasks to specialized agents.

- the runtime pipeline is defined in the CONFIGURATION environnement variable.

## What it exposes

- `GET /` - basic service metadata
- `GET /health` - health check
- `POST /chat` - main question endpoint


## How it works

The runtime graph is assembled at startup from `config.toml`.

For example:

1. The `generator` agent receives the user question, the database schema context, and the conversation memory.
2. It produces a MySQL query.
3. The database module executes the query and stores the results in the graph state.
4. The graph routes to the `explainer` agent, which turns the result into a concise French answer.
5. If the graph marks an error, it routes to the `exception` agent instead.

## Diagrams

- [Documentation index](docs/README.md)

Main implementation files:

- `app/main.py` - FastAPI app startup and graph initialization
- `app/api/routes.py` - HTTP routes
- `app/agents/` - agent registry, provider factory, and execution wrapper
- `app/modules/` - database and memory modules
- `app/prompt/` - prompts
- `app/workflows/` - LangGraph wiring and routing
- `app/tasks/` - scheduler helpers for memory reset and LLM refresh

## Requirements

- Python 3.9+
- A MySQL-compatible database
- One supported LLM provider:
  - `OPENAI_API_KEY`
  - `GROQ_API_KEY`
  - Ollama does not need an API key

## Environment

The application reads these variables at runtime:

- `CONFIGURATION` - path to the pipeline config file, usually `config.toml`
- `DB_USERNAME`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DATABASE`
- `OPENAI_API_KEY` - required if you use the OpenAI provider
- `GROQ_API_KEY` - required if you use the Groq provider
- `MEMORY_TIMEOUT_SECONDS` - optional inactivity timeout for memory cleanup

Example `.env`:

```env
CONFIGURATION=config.toml
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DATABASE=your_database_name

OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk-...
MEMORY_TIMEOUT_SECONDS=600
```

## Example Pipeline config

`config.toml` defines the agents and edges used by LangGraph.

Example flow:

- `generator` uses the `sql_prompt` and the `database` + `memory` modules
- `explainer` uses the `nlp_prompt` and the `memory` module
- `exception` uses the same natural-language prompt for fallback responses

If you need to change the model, provider, prompt, or attached modules, edit `config.toml`.

## Run locally

```bash
git clone https://github.com/Rayan-ouer/minimal-token-db-api.git
cd minimal-token-db-api

python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Example request

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Which region had the highest sales last year?",
    "session_id": 1
  }'
```

## Example responses

`POST /chat` returns the graph state. The important field is the final `output`, which contains the generated answer.

## Project structure

```text
app/
├── agents/     # agent registry, factory, and provider definitions
├── api/        # HTTP routes
├── modules/    # database and memory modules
├── prompt/     # prompts and schema metadata
├── schemas/    # typed state and request models
├── tasks/      # scheduler helpers
└── workflows/  # LangGraph graph and routing
```

## Notes

- The database connector expects MySQL connection details.
- The SQL prompt is strict about MySQL syntax and automatic `LIMIT` enforcement.
- The response prompt is in French and keeps answers concise.
