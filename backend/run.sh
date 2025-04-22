#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run FastAPI application with uvicorn
# --reload: Enable auto-reload for development
# --host 0.0.0.0: Allow connections from any IP
# --port 8000: Use port 8000
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 