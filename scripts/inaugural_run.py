#!/usr/bin/env python3
"""Inaugural Run Script for Noble Cause Steward.

This script orchestrates the Steward's first operational run, simulating
the inaugural deliberation between the Steward and the Gremium.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv(dotenv_path='backend/.env')

# Add the backend source to the Python path
backend_src = Path(__file__).parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_src))

# Import necessary modules
from noble_cause_steward.memory.chroma_provider import ChromaMemoryProvider
from noble_cause_steward.database.sql_provider import SQLProvider
from noble_cause_steward.research.web_adapter import WebAdapter
from noble_cause_steward.llm.open_router_adapter import OpenRouterAdapter
from noble_cause_steward.research.research_manager import ResearchManager


def load_prompt_file(filepath: str) -> str:
    """Load content from a prompt file.
    
    Args:
        filepath: Path to the prompt file relative to project root
        
    Returns:
        The content of the file as a string
    """
    project_root = Path(__file__).parent.parent
    full_path = project_root / filepath
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Could not find file {full_path}")
        return ""
    except Exception as e:
        print(f"Error reading file {full_path}: {e}")
        return ""


def main():
    """Main orchestration function for the inaugural run."""
    
    print("=" * 60)
    print("🏛️  NOBLE CAUSE STEWARD - INAUGURAL RUN")
    print("=" * 60)
    print()
    
    # Step 1: Instantiate Components
    print("📋 Initializing system components...")
    
    try:
        # Initialize memory provider
        memory_provider = ChromaMemoryProvider(collection_name="inaugural_memories")
        print("✅ ChromaMemoryProvider initialized")
        
        # Initialize database provider (using in-memory SQLite for demo)
        sql_provider = SQLProvider("sqlite:///:memory:")
        print("✅ SQLProvider initialized")
        
        # Initialize web adapter
        web_adapter = WebAdapter()
        print("✅ WebAdapter initialized")
        
        # Initialize OpenRouter adapter (requires OPENROUTER_API_KEY)
        openrouter_adapter = OpenRouterAdapter()
        print("✅ OpenRouterAdapter initialized")
        
        # Initialize research manager
        research_manager = ResearchManager(web_adapter, openrouter_adapter)
        print("✅ ResearchManager initialized")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please ensure OPENROUTER_API_KEY is set in backend/.env file.")
        return 1
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        return 1
    
    print()
    
    # Step 2: Load Prompts
    print("📖 Loading prompts...")
    
    # Load the manifest
    manifest_content = load_prompt_file("manifest.md")
    if not manifest_content:
        print("❌ Failed to load manifest.md")
        return 1
    print("✅ Manifest loaded")
    
    # Load the Gremium prompt
    gremium_prompt = load_prompt_file("prompts/gremium_prompt.md")
    if not gremium_prompt:
        print("❌ Failed to load gremium_prompt.md")
        return 1
    print("✅ Gremium prompt loaded")
    
    # Load the Steward's inaugural prompt
    steward_prompt = load_prompt_file("prompts/steward_inaugural_prompt.md")
    if not steward_prompt:
        print("❌ Failed to load steward_inaugural_prompt.md")
        return 1
    print("✅ Steward inaugural prompt loaded")
    
    print()
    
    # Step 3: Orchestrate the Flow
    print("🎭 Beginning inaugural deliberation...")
    print()
    
    # Combine the prompts for the LLM
    # System message: Gremium prompt + Manifest
    system_message = f"{gremium_prompt}\n\n## THE MANIFEST\n\n{manifest_content}"
    
    # User message: Steward's inaugural prompt
    user_message = steward_prompt
    
    print("🗣️  The Steward presents the inaugural prompt to the Gremium...")
    print()
    
    # Simulate the deliberation
    try:
        print("⏳ Awaiting Gremium response...")
        
        # Use OpenRouter to simulate the Gremium's response with proper system/user messages
        gremium_response = openrouter_adapter.generate_completion_with_system(
            system_message=system_message,
            user_message=user_message,
            model="openai/gpt-4o"
        )
        
        if gremium_response is None:
            print("❌ Failed to get response from the Gremium")
            return 1
        
        print("✅ Gremium has responded!")
        print()
        print("=" * 60)
        print("📜 GREMIUM DELIBERATION TRANSCRIPT")
        print("=" * 60)
        print()
        print(gremium_response)
        print()
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"❌ Error during deliberation: {e}")
        return 1
    
    # Step 4: Store key parts in memory
    print("💾 Storing deliberation in memory...")
    
    try:
        # Store the inaugural prompt
        memory_provider.add_memory(
            text=steward_prompt,
            metadata={
                "type": "steward_prompt",
                "session": "inaugural",
                "timestamp": time.time()
            }
        )
        
        # Store the Gremium's response
        memory_provider.add_memory(
            text=gremium_response,
            metadata={
                "type": "gremium_response",
                "session": "inaugural", 
                "timestamp": time.time()
            }
        )
        
        # Store the manifest for reference
        memory_provider.add_memory(
            text=manifest_content,
            metadata={
                "type": "manifest",
                "version": "1.0",
                "timestamp": time.time()
            }
        )
        
        print("✅ Deliberation stored in ChromaDB memory")
        
    except Exception as e:
        print(f"❌ Error storing memories: {e}")
        return 1
    
    print()
    
    # Step 5: Success message
    print("🎉 INAUGURAL RUN COMPLETED SUCCESSFULLY!")
    print()
    print("The Steward has successfully orchestrated the first deliberation")
    print("of the NobleCause.ai Gremium. The transcript has been recorded")
    print("and stored in the system's memory for future reference.")
    print()
    print("The Noble Cause Steward is now operational.")
    print()
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)