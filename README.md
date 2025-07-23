# NobleCause.ai

## Vision Statement

NobleCause.ai is envisioned as a living machine, a collective of wise intelligences working in harmony to drive positive change. It's a system designed to learn, adapt, and evolve, constantly striving to improve its ability to understand and address the world's most pressing challenges.

## Core Principles

*   **Radical Transparency:** All data, processes, and decisions are open and accessible for scrutiny and validation.
*   **Continuous Evolution:** The system is designed for constant learning and improvement, adapting to new information and challenges.
*   **Purpose-Driven Engineering:** Every aspect of the system is aligned with the overarching goal of contributing to the greater good.

## Architecture Overview

The NobleCause.ai system comprises the following key components:

*   **Observatory:** Gathers and analyzes data from various sources to identify opportunities for positive impact.
*   **Steward:** Manages and orchestrates the system's resources and activities, ensuring alignment with core principles.
*   **Gremium:** A deliberative body that provides guidance and oversight, ensuring ethical and responsible operation.
*   **Data Layer:** Provides storage and retrieval mechanisms for all data used by the system.

Key technologies used: SvelteKit, FastAPI, Python, OpenRouter, ChromaDB, PostgreSQL.

## Getting Started

⚠️ **IMPORTANT: Ensure the Docker Desktop application is running before executing any Docker commands.**

1.  **Prerequisites:** Ensure you have Docker installed on your system.
2.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd NobleCause.ai
    ```
3.  **Create .env file:** Create a `backend/.env` file and add your `OPENROUTER_API_KEY`.
4.  **Run the system:** Use the following command to build and start the entire system:
    ```bash
    docker-compose up --build
    ```

## Running the Inaugural Script

After the Docker containers are running, execute the `scripts/inaugural_run.py` script to initialize the system and see it in action:

```bash
docker exec -it backend python scripts/inaugural_run.py
```

## Development Methodology

We are committed to Test-Driven Development (TDD) to ensure the quality and reliability of our code.