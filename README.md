# Minimal Token Database API

A token-optimized intelligent chatbot API that converts natural language questions into SQL queries and returns human-readable responses with minimal LLM token consumption.
Built with LangChain's native framework for universal API compatibility.

## 💡 Why Minimal Token?

### Traditional LLM Database Queries

Traditional approaches to querying databases with LLMs consume a lot of tokens:

```
Traditional Approach:
User Question (10 tokens)
  → Send entire database schema (5000+ tokens)
  → Send conversation history (2000+ tokens)
  → Get SQL query (100 tokens)
  → Send full SQL results (3000+ tokens)
  → Get formatted response (200 tokens)
────────────────────────────────────────────
Total: ~10,300+ tokens per query.
```

### Solution: Token-Optimized Architecture

**Minimal Token DB API** dramatically reduces token consumption :

```
Minimal Token Approach:
User Question (10 tokens)
  → Optimized schema context (200 tokens)
  → Smart conversation window (150 tokens)
  → Get SQL query (100 tokens)
  → Compressed results (500 tokens)
  → Get formatted response (200 tokens)
────────────────────────────────────────────
Total: ~1,160 tokens per query.
```

**Result: ~89% token reduction! **

### How i thinks it

1. **Selective Schema Loading**
   - Only sends relevant table descriptions based on question context
   - Eliminates unnecessary schema information
   - Dynamic schema filtering per query

2. **Conversation Memory Optimization**
   - Maintains only the last 3 Q&A pairs per session(You can change it easily)
   - Automatically prunes old context(You can desactive it or change it)
   - Smart relevance-based history selection

3. **Result Compression**
   - Summarizes large result sets
   - Returns only essential data points
   - Intelligent data aggregation

4. **Dual-Agent Specialization**
   - Separate lightweight agents for SQL and NLP
   - Each llm receives only what it needs
   - No redundant context passing

### Universal API and AI Prodiver Compatibility

Built with **LangChain's native framework**, this architecture works with:

- **OpenAI** (GPT-4, GPT-3.5)
- **Anthropic** (Claude)
- **Groq** (Llama, Mixtral, Gemma)
- **Google** (Gemini, PaLM)
- **AWS Bedrock** (Titan, Claude)
- **HuggingFace Models**
- **Ollama**

**Simply change the API key if needed, model name and provider name**

## 🏗 Architecture

The system uses a token-optimized dual-agent architecture:

```
┌─────────────────────┐
│   User Question     │ ← 10 tokens
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│   Smart Context Builder         │
│   • Relevant schema only        │ ← 200 tokens
│   • Last 3 Q&A pairs            │ ← 150 tokens
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────┐
│   SQL Agent (LLM)   │ ← Generates MySQL query
└──────────┬──────────┘ ← 100 tokens output
           │
           ▼
┌─────────────────────┐
│   Database          │ ← Executes query
│   Execution         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│   Result Compressor             │
│   • Summarizes large sets       │ ← 500 tokens
│   • Extracts key data           │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────┐
│   NLP Agent (LLM)   │ ← Formats natural language
└──────────┬──────────┘ ← 200 tokens output
           │
           ▼
┌─────────────────────┐
│   User Response     │
└─────────────────────┘

Total: ~1,160 tokens (89% reduction!)
```

### The Two Specialized Agents

1. **SQL Agent** 🔍
   - Receives only relevant schema context
   - Understands database structure
   - Generates syntactically correct MySQL queries
   - Optimizes query performance
   - Handles complex joins and aggregations

2. **NLP Agent** 💬
   - Receives only compressed results
   - Translates SQL results into natural language
   - Formats responses professionally
   - Adapts tone and style
   - Handles errors gracefully


## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.9+** installed on your machine
- **Docker** and **Docker Compose** (recommended for deployment)
- **SQL database** or compatible database
- **LLM API Key**
## 🚀 Installation

### Option 1: Docker (Recommended) 🐳

#### 1. Clone the repository

```bash
git clone https://github.com/Rayan-ouer/minimal-token-db-api.git
cd minimal-token-db-api
```

#### 2. Create `.env` file

Create a `.env` file at the root of the project:

```env
# Database Configuration
AI_USERNAME=username
AI_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=database_name

# AI Provider (choose one)
AI_PROVIDER=openai
AI_MODEL=gpt-5-mini

# API Keys (Optional, ollama for example does not need it)
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# Optional
MEMORY_TIMEOUT_SECONDS=600  # Default: 10 minutes
```

#### 3. Install Provider Dependencies

The required provider library is already in `requirements.txt`. If you're adding a new provider:
```bash
# Already included:
# - langchain-groq
# - langchain-openai
# - langchain-anthropic
# - langchain-ollama

pip install -r requirements.txt

#### 4. add your ai provider library in requirement.txt
langchain-openai
langchain-ollama

#### 3. Launch with Docker Compose

```bash
# Build Docker image
docker compose build

# Start containers
docker compose up

# Check logs
docker compose logs
```

### Option 2: Local Installation 💻

#### 1. Clone the repository

```bash
git clone https://github.com/Rayan-ouer/minimal-token-db-api.git
cd minimal-token-db-api
```

#### 2. Create virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate environment (Linux/Mac)
source venv/bin/activate

# Activate environment (Windows)
venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Launch the application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Database Schema

The system is pre-configured for inventory management databases with tables:

- **items**: Products and commercial data
- **stocks**: Stock levels per store
- **stock_movements**: Inbound/outbound history
- **delivery_notes**: Delivery documents
- **invoices**: Issued invoices
- **vehicles**: Vehicle data

#### Adapting to Your Schema

To use your own database schema:

1. Open `app/prompt/table_info.py`
2. Modify table descriptions to match your structure
3. Update example queries if necessary
4. Restart the application

### Main API Endpoint: `POST /predict`

#### Request

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Which products are out of stock?",
    "session_id": 12345
  }'
```

#### Response

```json
{
  "status": "success",
  "response": "Currently, there are 3 products out of stock: Motor Oil 5W30 (quantity: 0), K&N Air Filter (quantity: 0), and 12V 70Ah Battery (quantity: 0).",
}
```

### Request Parameters

| Parameter | Type | Description |
|-----------|------|------------
| `question` | string | Natural language question |
| `session_id` | integer | Session identifier for context |

### HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success - Response returned |
| `400` | Parameter validation error |
| `500` | Internal server error |

## 💡 Example Questions

```bash
# Check stock shortages
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show me items below minimum stock level",
    "session_id": 1
  }'

# Total stock quantity
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the total quantity of parts in stock?",
    "session_id": 1
  }'

# Stock by location
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show stock levels by warehouse location",
    "session_id": 1
  }'
```

## Project Structure

```
app/
├── db/              # Database connection & query execution
├── prompt/          # AI prompts & schema definitions
├── schemas/         # Request/response models
├── services/        # AI providers, memory, agent factory
└── tasks/           # Background jobs & scheduler
```

### Key Modules Description

### 1. AI Agents (`app/services/`)

#### SQL Agent
- **Purpose:** Convert natural language → MySQL queries
- **Temperature:** 0.1 (deterministic)
- **Rules:** MySQL-only syntax, automatic LIMIT enforcement, table alias requirement

#### NLP Agent
- **Purpose:** Convert SQL results → Natural French responses
- **Temperature:** 0.3 (natural variation)
- **Rules:** Never mention technical terms (SQL, database), conversational tone, concise (2-3 sentences)

### 2. Chat Memory (`app/services/chat.py`)

```python
memory = ChatMemory()

# Session management
memory.add_user_message(session_id, question)
memory.add_ai_message(session_id, response)

# Keep last 3 Q&A pairs
memory.rotate_history(session_id, max_questions=3)

# Cleanup
memory.clear_history_by_id(session_id)
memory.clear_all_sessions()
```

### 3. Database Layer (`app/db/database.py`)

**Key Functions:**
- `create_engine_for_sql_database()` - SQLAlchemy engine with pooling
- `verify_and_extract_sql_query()` - Validate and enforce LIMIT
- `execute_queries()` - Execute and return structured results
- `is_empty_result()` - Check for empty query results

### 4. Agent Factory (`app/services/factories.py`)

```python
agent = init_ai_agent(
    model_config={"temperature": 0.1, "max_retries": 2},
    engine=database_engine,
    prompt_settings=prompt_template
)
```

## Customization

### Adding New AI Provider

Edit `app/services/ai_providers.py`:

```python
PROVIDERS = {
    "your_provider": {
        "class": YourProviderClass,
        "key": "YOUR_API_KEY_ENV_VAR"  # or None for local
    }
}
```

### Modifying Database Schema

Edit `app/prompt/table_info.py`:

```python
table_info = {
    "your_table": {
        "description": "Table purpose",
        "columns": {
            "id": "Column description",
            # ... more columns
        }
    }
}
```

### Customizing Prompts

Edit `app/prompt/prompt.py`:

**SQL Agent:** Modify `sql_prompt` for query generation rules  
**NLP Agent:** Modify `nlp_prompt` for response formatting

---

## Background Jobs

### Scheduler (`app/tasks/scheduler.py`)

Automatic tasks using APScheduler:

1. **Memory Cleanup** - Every 1 minute
   - Resets inactive sessions (default: 10 min timeout)
   
2. **LLM Reset** - Daily at 00:00 and 12:00
   - Reinitializes agents to prevent degradation

### Manual Triggers (`app/tasks/jobs.py`)

```python
# Reset all memory
reset_agents_memory(app)

# Reset specific session
reset_memory_user(app, session_id)

# Check inactive sessions
check_last_request_per_user(app, timeout_seconds)

# Reset LLM agents
reset_llm(app)
```

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Invalid SQL | Returns empty result, NLP explains gracefully |
| DB Connection | NLP agent provides user-friendly error message |
| Empty Results | Returns "no matching item" to NLP agent |
| Critical Failure | 500 error with generic message |

---

## Memory Management

### Session History
- Each session maintains independent conversation history
- Automatic rotation: keeps last 3 Q&A pairs (6 messages total)
- Prevents context overflow in long conversations

### Cleanup Strategy
- **Timeout-based:** Inactive sessions cleared after configurable period
- **Scheduled:** Full reset at midnight and noon
- **Manual:** On-demand via API shutdown or manual trigger

---


## 🔌 API Endpoints

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
  - Interactive interface to test the API
  - Detailed endpoint documentation
  - Request/response examples

- **ReDoc**: `http://localhost:8000/redoc`
  - Alternative, more readable documentation
  - API overview

### Main Endpoint

#### `POST /predict`

Processes a natural language question and returns a response.

**Request Body:**

```json
{
  "question": "string",
  "session_id": 0
}
```

**Success Response:**

```json
{
  "status": "success",
  "response": "string",
}
```

**Error Response:**

```json
{
  "status": "error",
  "response": "Error description"
}
```

### Health Check

#### `GET /health`

Checks the API health status.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

## Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern web framework
- **[LangChain](https://python.langchain.com/)**: LLM orchestration
- **[Groq](https://groq.com/)**: LLM inference
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: Database ORM
- **[Pydantic](https://pydantic.dev/)**: Data validation
- **[Docker](https://www.docker.com/)**: Containerization

## Author

**Rayan**
- GitHub: [@Rayan-ouer](https://github.com/Rayan-ouer)
