# News Pulse

News Pulse is a web application that aggregates and analyzes political content from various news sources. It helps users understand different political perspectives and find common ground in news coverage.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/newspulse.git
   cd newspulse
   ```

2. **Set up the backend**:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Set up the frontend**:
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

#### Option 1: Using Docker (Recommended)

1. **Start all services**:
   ```bash
   docker-compose up -d
   ```

2. **Access the application**:
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

#### Option 2: Manual Setup

1. **Start the backend**:
   ```bash
   # Terminal 1
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uvicorn app.main:app --reload
   ```

2. **Start the frontend**:
   ```bash
   # Terminal 2
   cd frontend
   ng serve
   ```

3. **Access the application**:
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000

## 🧪 Testing

### Backend Tests

```bash
# Navigate to the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run all tests
python -m unittest discover tests

# Run specific test files
python -m unittest tests/test_news_client.py
python -m unittest tests/test_visualization.py
```

### Frontend Tests

```bash
# Navigate to the frontend directory
cd frontend

# Run tests with Karma
ng test
```

## 📚 API Testing Guide

### Data Collection

```bash
# Basic topic search
curl -X POST "http://localhost:8000/api/v1/articles/collect?topic=politics"

# Topic search with language filter
curl -X POST "http://localhost:8000/api/v1/articles/collect?topic=politics&language=es"

# Topic search with date range
curl -X POST "http://localhost:8000/api/v1/articles/collect?topic=politics&days_back=30"
```

### Data Retrieval

```bash
# View all articles
curl "http://localhost:8000/api/v1/articles/"

# Filter articles by search term
curl "http://localhost:8000/api/v1/articles/?search=democrat"

# Filter by date range
curl "http://localhost:8000/api/v1/articles/?start_date=2024-01-01&end_date=2024-03-31"

# Filter by source
curl "http://localhost:8000/api/v1/articles/?source=CNN"
```

## 🛠️ Tech Stack

- **Frontend**: Angular 17+
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Containerization**: Docker

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
