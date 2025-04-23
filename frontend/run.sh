#!/bin/bash

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Run Angular development server
# --open: Open browser automatically
# --port 4200: Use port 4200
# --host 0.0.0.0: Allow connections from any IP
ng serve --open --port 4200 --host 0.0.0.0 