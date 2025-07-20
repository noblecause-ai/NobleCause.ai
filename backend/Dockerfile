# Use Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Configure Poetry: don't create virtual environment, install dependencies globally
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Copy Poetry configuration files
COPY pyproject.toml ./

# Install dependencies
RUN poetry install --only=main && rm -rf $POETRY_CACHE_DIR

# Copy the rest of the application code
COPY src/ ./src/

# Expose port 8000
EXPOSE 8000

# Set the Python path to include src directory
ENV PYTHONPATH=/app/src

# Command to run the FastAPI application
CMD ["poetry", "run", "uvicorn", "noble_cause_steward.main:app", "--host", "0.0.0.0", "--port", "8000"]