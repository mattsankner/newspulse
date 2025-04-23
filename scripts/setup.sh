#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting setup process..."

# Check for required tools
echo "🔍 Checking for required tools..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed"; exit 1; }
command -v createdb >/dev/null 2>&1 || { echo "❌ PostgreSQL is required but not installed"; exit 1; }

# Get current user
CURRENT_USER=$(whoami)
echo "👤 Current user: $CURRENT_USER"

# Create and setup PostgreSQL database
echo "🗄️ Setting up PostgreSQL database..."
createdb political_content 2>/dev/null || echo "ℹ️ Database already exists or connection failed"

# Grant permissions to current user
echo "🔑 Setting up database permissions..."
psql -d political_content -c "GRANT ALL PRIVILEGES ON DATABASE political_content TO $CURRENT_USER;" 2>/dev/null || true

# Setup Python backend
echo "🐍 Setting up Python backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
echo "Installing Python dependencies..."
pip install -r requirements.txt
cd ..

# Setup Angular frontend
echo "🅰️ Setting up Angular frontend..."
cd frontend
echo "Installing Node.js dependencies..."
npm install
cd ..

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating .env file..."
    echo "DATABASE_URL=postgresql://$CURRENT_USER@localhost:5432/political_content" > backend/.env
    echo "NEWS_API_KEY=" >> backend/.env
    echo "⚠️ Please edit backend/.env to add your News API key"
fi

# Make run scripts executable
echo "🔧 Making run scripts executable..."
chmod +x backend/run.sh
chmod +x frontend/run.sh

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  Backend: cd backend && ./run.sh"
echo "  Frontend: cd frontend && ./run.sh"
echo ""
echo "The application will be available at:"
echo "  Frontend: http://localhost:4200"
echo "  Backend API: http://localhost:8000"
echo "  API Documentation: http://localhost:8000/docs"
