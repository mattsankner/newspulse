#!/bin/bash

# Function to find and activate virtual environment
activate_venv() {
    # Common virtual environment names + my own
    local venv_names=("pulse-env" "venv" "env"  ".venv")
    
    for venv_name in "${venv_names[@]}"; do
        if [ -d "$venv_name" ]; then
            echo "Activating virtual environment: $venv_name"
            source "$venv_name/bin/activate"
            return 0
        fi
    done
    
    # If no virtual environment found, check if one is already active
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "Using already activated virtual environment: $VIRTUAL_ENV"
        return 0
    fi
    
    echo "❌ No virtual environment found. Please create one with:"
    echo "python -m venv <venv_name>"
    echo "Then activate it with:"
    echo "source <venv_name>/bin/activate"
    exit 1
}

# Try to activate virtual environment
activate_venv()

# Run FastAPI application with uvicorn
# --reload: Enable auto-reload for development
# --host 0.0.0.0: Allow connections from any IP (useful for docker)
# --port 8000: Use port 8000
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 