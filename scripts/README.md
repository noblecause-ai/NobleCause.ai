# Noble Cause Steward Scripts

This directory contains operational scripts for the Noble Cause Steward system.

## Inaugural Run Script

The [`inaugural_run.py`](inaugural_run.py) script orchestrates the Steward's first operational run, simulating the inaugural deliberation between the Steward and the Gremium.

### Prerequisites

1. **Install Dependencies**: Ensure all backend dependencies are installed:
   ```bash
   cd backend
   poetry install
   ```

2. **Configure Environment Variables**: The script requires an OpenRouter API key. Create a `backend/.env` file with your API key:
   ```bash
   # Create the .env file in the backend directory
   echo "OPENROUTER_API_KEY=your_openrouter_api_key_here" > backend/.env
   ```
   
   Or manually create `backend/.env` and add:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```
   
   You can get an API key from: https://openrouter.ai/keys

### Running the Script

From the project root directory:

```bash
python scripts/inaugural_run.py
```

### What the Script Does

1. **Initializes Components**: Creates instances of all system components:
   - [`ChromaMemoryProvider`](../backend/src/noble_cause_steward/memory/chroma_provider.py) for memory storage
   - [`SQLProvider`](../backend/src/noble_cause_steward/database/sql_provider.py) for structured data
   - [`WebAdapter`](../backend/src/noble_cause_steward/research/web_adapter.py) for web content fetching
   - [`OpenRouterAdapter`](../backend/src/noble_cause_steward/llm/open_router_adapter.py) for LLM communication
   - [`ResearchManager`](../backend/src/noble_cause_steward/research/research_manager.py) for research coordination

2. **Loads Prompts**: Reads the system prompts:
   - [`manifest.md`](../manifest.md) - The foundational document
   - [`prompts/gremium_prompt.md`](../prompts/gremium_prompt.md) - Gremium member instructions
   - [`prompts/steward_inaugural_prompt.md`](../prompts/steward_inaugural_prompt.md) - The inaugural address

3. **Orchestrates Deliberation**: 
   - Combines the Gremium prompt and Manifest as the system message
   - Uses the Steward's inaugural prompt as the user message
   - Calls the OpenRouter API to simulate the Gremium's response

4. **Stores Results**: Saves the deliberation transcript and key documents in ChromaDB memory for future reference

### Expected Output

The script will display:
- Initialization status for each component
- Progress messages during the deliberation
- The complete Gremium response transcript
- Confirmation of successful memory storage

### Troubleshooting

- **Missing API Key**: Ensure `OPENROUTER_API_KEY` is set in the `backend/.env` file
- **Import Errors**: Verify backend dependencies are installed with `poetry install`
- **ChromaDB Issues**: The script uses an in-memory ChromaDB instance, so no external database setup is required

This script serves as both a functional test of the system components and the ceremonial first activation of the Noble Cause Steward.