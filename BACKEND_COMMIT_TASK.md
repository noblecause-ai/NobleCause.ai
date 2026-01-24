# Backend Testing and Commit Task for Claude

**Priority**: CRITICAL - Complete before frontend work

## Objective
Test all backend changes, fix issues, and commit backend changes.

## Phase 1: Testing

### Step 1: Environment Setup
cd /home/ubuntu/NobleCause.ai/backend
cat .env | grep OPENROUTER_API_KEY
poetry install

### Step 2: Run Tests
poetry run pytest tests/test_websocket.py -v
poetry run pytest tests/deliberation/test_langgraph_deliberation.py -v
poetry run pytest -v

### Step 3: Manual WebSocket Test
Start server: poetry run uvicorn noble_cause_steward.main:app --host 0.0.0.0 --port 8000
Test WebSocket at ws://localhost:8000/ws/deliberate
(For remote testing, use your server's IP address from environment or configuration)

## Phase 2: Commit (After Tests Pass)

### Stage Files
cd /home/ubuntu/NobleCause.ai
git add backend/src/noble_cause_steward/deliberation/*.py
git add backend/src/noble_cause_steward/llm/async_open_router_adapter.py
git add backend/tests/test_websocket.py
git add backend/tests/deliberation/test_langgraph_deliberation.py
git add backend/src/noble_cause_steward/main.py
git add backend/pyproject.toml
git add backend/src/noble_cause_steward/database/sql_models.py
git add backend/src/noble_cause_steward/memory/chroma_provider.py
git add backend/tests/memory/test_chroma_provider.py
git add .gitignore

### Commit
git commit -m "feat: Implement LangGraph deliberation with WebSocket streaming"

### Push
git push origin master

## Update Coordination
After committing, update AGENT_COORDINATION.md with commit hash.