# Frontend Task for Aider/Gemini (Frontend Agent)

**Date**: 2026-01-23  
**Priority**: HIGH - Wait for backend commit first

## IMPORTANT: Wait for Backend Commit

**DO NOT START** until backend agent (Claude) has:
1. âœ… Completed all backend tests
2. âœ… Committed backend changes
3. âœ… Updated AGENT_COORDINATION.md with commit status

**Check status:**
\\\ash
cd /home/ubuntu/NobleCause.ai
cat AGENT_COORDINATION.md | grep -A 5 " Backend Status\
git log --oneline -1 # Check if backend commit exists
\\\

## Current Status

- âœ… WebSocket contract documentation ready (docs/websocket_contract.md)
- âœ… Frontend WebSocket service exists (frontend/src/lib/services/websocketService.ts)
- âœ… Deliberation store updated with WebSocket types
- âŒ Tailwind CSS missing (needs installation)
- âŒ Observatory UI not implemented
- âš ï¸ Deliberation component still uses SSE (needs WebSocket update)

## Your Tasks (After Backend Commit)

### 1. Verify Backend is Committed
\\\ash
cd /home/ubuntu/NobleCause.ai
git log --oneline -1
# Should see commit with \feat: Implement LangGraph deliberation with WebSocket streaming\
\\\

### 2. Review Documentation
\\\ash
cat docs/websocket_contract.md
cat docs/gap_analysis.md
cat AGENT_COORDINATION.md
\\\

### 3. Install Tailwind CSS (CRITICAL)
\\\ash
cd frontend
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Configure tailwind.config.js
cat > tailwind.config.js << 'TAILEOF'
/** @type {import('tailwindcss').Config} */
export default {
 content: ['./src/**/*.{html,js,svelte,ts}'],
 theme: {
 extend: {},
 },
 plugins: [],
}
TAILEOF

# Add Tailwind directives to app.css or create it
mkdir -p src
cat > src/app.css << 'CSSEOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
CSSEOF
\\\

### 4. Build Observatory UI (CRITICAL)

The Observatory is a 2D \Stage Manager\ interface, not a dashboard. It should:

- Show transitions between \The Office\ and \The Gremium Hall\
- Display deliberation as a live narrative
- Use speech bubbles for agent responses
- Show inner monologue/thoughts
- Create visual storytelling experience

**Key Components to Create:**
- \src/routes/+layout.svelte\ - Stage Manager for scene transitions
- \src/lib/components/Observatory.svelte\ - Main Observatory interface
- \src/lib/components/OfficeScene.svelte\ - The Office scene
- \src/lib/components/GremiumHallScene.svelte\ - The Gremium Hall scene
- \src/lib/components/SpeechBubble.svelte\ - Agent speech bubbles
- \src/lib/components/InnerMonologue.svelte\ - Inner thoughts display

### 5. Update Deliberation Component

Replace SSE code with WebSocket:
- Remove EventSource usage
- Use websocketService.ts
- Connect to ws://{VITE_API_URL}/ws/deliberate
- Handle all WebSocket message types from contract

### 6. Integrate WebSocket Service

- Connect websocketService to Observatory UI
- Display real-time deliberation updates
- Show agent responses as they arrive
- Handle connection states (connecting, connected, error)

### 7. Test and Update Status

- Test WebSocket connection
- Verify all message types display correctly
- Update AGENT_COORDINATION.md with progress

## Expected Outcomes

- Tailwind CSS installed and working
- Observatory UI displays 2D interface
- Transitions work between Office and Gremium Hall
- WebSocket connects successfully
- All deliberation messages display correctly
- Visual narrative elements work (speech bubbles, monologue)

## Important Notes

- Wait for backend commit before starting
- Follow docs/websocket_contract.md exactly
- Observatory is narrative interface, not dashboard
- Use Svelte 5 (Runes) - already in package.json
- Update coordination board with progress

## Reference Documents

- docs/websocket_contract.md - WebSocket protocol
- docs/gap_analysis.md - What's missing
- AGENT_COORDINATION.md - Coordination board
- MVP_REQUIREMENTS.md - MVP requirements
