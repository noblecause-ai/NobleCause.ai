# Agent Coordination Board

**Last Updated**: 2026-01-23  
**Status**: Active Development - WebSocket/LangGraph Architecture - API Key Configured

## Current Agents

1. **Claude Code** (Backend Agent) - Session: `noble_claude`
   - Focus: Backend API, LangGraph deliberation, WebSocket endpoint
   - Working Directory: `backend/`
   - Architecture: LangGraph state machine (Propose → Critique → Synthesize)

2. **Aider (Gemini 3)** (Frontend Agent) - Session: `noble_aider` (or similar)
   - Focus: Frontend UI, Observatory interface, WebSocket integration
   - Working Directory: `frontend/`
   - Architecture: Svelte 5 with Tailwind CSS, WebSocket service

## Active Tasks

### Backend Tasks (Claude Code) - **IN PROGRESS: Testing & Commit**
- [x] **COMPLETED**: OpenRouter API key configured in `backend/.env` (permissions: 600)
- [ ] **CRITICAL**: Test WebSocket endpoint `/ws/deliberate` with OpenRouter API key
- [ ] Verify LangGraph deliberation executes correctly (3 rounds)
- [ ] Test WebSocket message streaming (all message types)
- [ ] Ensure error handling for WebSocket connections
- [x] **COMPLETED**: Environment variable configured (OPENROUTER_API_KEY in .env)
- [ ] Test deliberation repository (database persistence)
- [ ] Run and fix WebSocket tests (`test_websocket.py`)
- [ ] Run and fix LangGraph tests (`test_langgraph_deliberation.py`)
- [ ] Check database connection health
- [ ] **CRITICAL**: Commit backend changes after all tests pass
- [ ] Push backend changes to repository

### Frontend Tasks (Aider/Gemini) - **WAITING: Backend Commit First**
- [ ] **WAITING**: Backend commit must complete before starting
- [ ] **CRITICAL**: Install and configure Tailwind CSS (after backend commit)
- [ ] **CRITICAL**: Build Observatory UI (2D Stage Manager interface)
- [ ] Implement transitions between "The Office" and "The Gremium Hall"
- [ ] Update Deliberation component to use WebSocket (not SSE)
- [ ] Integrate WebSocket service with Observatory UI
- [ ] Add proper error states and loading indicators
- [ ] Verify WebSocket connection configuration (VITE_API_URL)
- [ ] Test responsive design with Tailwind
- [ ] Implement visual narrative elements (speech bubbles, inner monologue)

### Shared Tasks
- [ ] **CRITICAL**: Pull and sync server changes (LangGraph, WebSocket code)
- [ ] Verify WebSocket contract adherence (`docs/websocket_contract.md`)
- [ ] Test end-to-end: Frontend WebSocket → Backend LangGraph → Database
- [ ] Verify docker-compose.yml works with new architecture
- [ ] Ensure all health checks pass
- [ ] Run complete test suite and fix failures
- [ ] Test with new OpenRouter API key

## Current Status

### Backend Status
- **Last Activity**: 2026-01-23 - Task delegated: Testing and committing backend changes
- **Current Focus**: Testing WebSocket endpoint and LangGraph deliberation (see BACKEND_COMMIT_TASK.md)
- **Blockers**: None - API key configured, ready for testing
- **Task File**: BACKEND_COMMIT_TASK.md (comprehensive testing and commit instructions)

### Frontend Status
- **Last Activity**: 2026-01-23 - Task delegated: Waiting for backend commit
- **Current Focus**: Waiting for backend testing and commit to complete
- **Blockers**: Backend commit must complete first (see FRONTEND_AGENT_TASK.md)
- **Task File**: FRONTEND_AGENT_TASK.md (includes wait instruction)

## Communication Protocol

### Before Starting Work
1. Read this file
2. Check `MVP_REQUIREMENTS.md` for requirements
3. Check git status for uncommitted changes
4. Announce your intended work in the "Current Focus" section

### After Completing Work
1. Update your status section
2. Mark completed tasks
3. Commit changes with clear messages
4. Test your changes

### When You Need Coordination
1. Add a note in the "Coordination Needed" section below
2. Wait for acknowledgment or proceed if urgent
3. Update this file when resolved

## Coordination Needed

_Use this section to request coordination or report conflicts_

- [No current coordination requests]

## Recent Changes

### 2026-01-23
- **DELEGATION**: Tasks assigned to both agents via tmux
- Backend: Testing and commit task created (BACKEND_COMMIT_TASK.md)
- Frontend: Task updated to wait for backend commit (FRONTEND_AGENT_TASK.md)
- OpenRouter API key configured on server (`backend/.env`)
- WebSocket contract documentation created
- Gap analysis completed
- Testing checklist prepared

### 2026-01-22
- Created coordination system
- Defined MVP requirements
- Established agent communication protocol

## Architecture Overview

### Backend (Claude)
- **Communication**: WebSocket at `/ws/deliberate` (NOT SSE)
- **State Management**: LangGraph with 3-round flow
- **Rounds**: Propose (1) → Critique (2) → Synthesize (3)
- **Streaming**: Real-time JSON messages via WebSocket
- **Contract**: See `docs/websocket_contract.md`

### Frontend (Gemini)
- **Framework**: Svelte 5 (Runes) with SvelteKit
- **Styling**: Tailwind CSS (needs installation)
- **Interface**: Observatory (2D Stage Manager, not dashboard)
- **Communication**: WebSocket service (`websocketService.ts`)
- **Store**: `deliberationStore.ts` with WebSocket message types

## Git Status

**Current Branch**: master  
**Last Commit**: 87eee18 feat: Implement Live Observatory with SSE and Deliberation UI

**Uncommitted Changes on Server** (NEED TESTING BEFORE COMMIT):
- `backend/src/noble_cause_steward/deliberation/langgraph_deliberation.py` - LangGraph implementation
- `backend/src/noble_cause_steward/deliberation/state.py` - State management
- `backend/src/noble_cause_steward/deliberation/repository.py` - Database persistence
- `backend/src/noble_cause_steward/llm/async_open_router_adapter.py` - Async adapter
- `backend/src/noble_cause_steward/main.py` - WebSocket endpoint `/ws/deliberate`
- `backend/pyproject.toml` - Added LangGraph and langchain-core
- `frontend/src/lib/services/websocketService.ts` - WebSocket service
- `frontend/src/lib/stores/deliberationStore.ts` - Updated with WebSocket types
- `backend/tests/test_websocket.py` - WebSocket tests
- `backend/tests/deliberation/test_langgraph_deliberation.py` - LangGraph tests

## Next Steps

### Immediate (Backend First)
1. **Backend (Claude)**: 
   - Follow BACKEND_COMMIT_TASK.md
   - Test WebSocket endpoint with OpenRouter API key
   - Run all tests and fix any failures
   - Commit backend changes after tests pass
   - Update this file with commit hash and status
2. **Frontend (Gemini)**: 
   - Wait for backend commit (check git log)
   - Once backend is committed, follow FRONTEND_AGENT_TASK.md
   - Install Tailwind CSS
   - Build Observatory UI (2D interface)
   - Integrate WebSocket service

### After Backend Commit
3. **Both**: 
   - Test end-to-end WebSocket connection
   - Verify contract adherence
   - Fix integration issues
4. **Goal**: Working MVP with WebSocket deliberation and Observatory UI

## Commit Workflow

**Backend Commit Process:**
1. Complete all tests
2. Stage backend files (see BACKEND_COMMIT_TASK.md)
3. Commit with message: "feat: Implement LangGraph deliberation with WebSocket streaming"
4. Push to origin/master
5. Update this file with commit hash
6. Notify frontend agent to proceed

## Important Notes

- **WebSocket Contract**: Both agents MUST follow `docs/websocket_contract.md` exactly
- **No Hardcoded Secrets**: Always use environment variables (OPENROUTER_API_KEY in .env)
- **Test Before Commit**: Server code is untested - must test thoroughly before committing
- **Communication**: Update this file when working on shared components
- **File Ownership**: 
  - Backend agent: `backend/` directory (priority)
  - Frontend agent: `frontend/` directory (priority)
  - Shared: `docker-compose.yml`, `docs/`, coordination files
- **Architecture**: WebSocket (NOT SSE) - old SSE code should be removed/replaced
- **State Machine**: LangGraph manages 3-round deliberation flow automatically
