# 📰 News Pulse

**News Pulse** analyzes news articles on political topics, categorizes them based on political alignment, and identifies common ground using advanced AI techniques.

---

## 🚀 Features

- **Content Aggregation**: Fetches political news articles using NewsAPI.
- **Political Categorization**: Classifies articles into left, right, and center stances.
- **Common Ground Detection**: Utilizes Retrieval-Augmented Generation (RAG) AI to find consensus points.
- **Intuitive UI**: Presents results clearly in a responsive three-column layout.

---

## 🛠️ Tech Stack

| Layer              | Technology                                    |
|--------------------|-----------------------------------------------|
| **Frontend**       | Angular, Tailwind CSS                         |
| **Backend**        | FastAPI (Python)                              |
| **Database**       | PostgreSQL with pgvector                      |
| **AI Models**      | Hugging Face (classification & embeddings)    |

---

## 📐 Project Architecture

```plaintext
News Pulse
├── Frontend (Angular)
│   ├── Components
│   │   ├── Dashboard
│   │   ├── Article Card
│   │   ├── Stance Card
│   │   └── Column Components
│   ├── Services
│   └── Models
├── Backend (FastAPI)
│   ├── API Endpoints
│   ├── Database Models
│   └── Services
└── Database (PostgreSQL)
```

---

## 🗃️ Database Layer

**PostgreSQL + SQLAlchemy** stores and manages article data, political classifications, and consensus insights.

**Models:**
- `ArticleModel`: Stores news articles.
- `ClassificationModel`: Political stance classifications.
- `ConsensusModel`: Consensus data points.

### 📍 Database Setup

```bash
createdb political_content
psql political_content

# Verify tables (after running the app)
\dt  # Should list: articles, classifications, consensus
```

---

## ⚙️ Backend Layer

Powered by **FastAPI**, provides robust API endpoints and business logic for data management.

**Components:**
- API Routes (`/api/v1/articles/`)
- Database Session Management
- Comprehensive Error Handling

### 📍 Running the Backend

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload

# Test API endpoints
curl http://localhost:8000/api/v1/articles/

# Check API documentation
# Open in browser: http://localhost:8000/docs
```

---

## 💻 Frontend Layer

Angular frontend delivers intuitive user experience and clear data presentation.

**Components:**
- `DashboardComponent`: Main interface and search capability.
- `ArticleCardComponent`: Displays articles.
- `StanceCardComponent`: Visualizes political stance.
- Column Components (Left, Center, Right): Organize article content.

### 📍 Running the Frontend

```bash
cd frontend
npm install
ng serve

# Open in browser: http://localhost:4200
```

---

## 🐳 Docker Setup

Enables containerization for simplified deployment and management.

### 📍 Docker Commands

```bash
docker-compose up --build

# Verify running containers
docker ps

# Test services
curl http://localhost:8000  # Backend
curl http://localhost:4200  # Frontend
```

---

## 🚦 Run Scripts (Recommended)

Streamlined scripts to simplify development and deployment.

### 📄 Backend Script (`backend/run.sh`)

```bash
#!/bin/bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 📄 Frontend Script (`frontend/run.sh`)

```bash
#!/bin/bash
npm install
ng serve --open
```

### 📄 Setup Script (`setup.sh`)

```bash
#!/bin/bash

# PostgreSQL database setup
echo "Creating PostgreSQL database..."
createdb political_content 2>/dev/null || echo "Database exists or connection issue."

# Python virtual environment setup
echo "Setting up Python environment..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Angular dependencies setup
echo "Installing Angular dependencies..."
cd frontend
npm install
cd ..

# Create .env file
echo "Checking .env file..."
if [ ! -f backend/.env ]; then
  cp backend/.env.template backend/.env
  echo "Edit backend/.env with your NewsAPI key."
fi

echo "✅ Setup complete! Use:"
echo "🔹 Backend: cd backend && ./run.sh"
echo "🔹 Frontend: cd frontend && ./run.sh"
```

Make scripts executable:

```bash
chmod +x backend/run.sh frontend/run.sh setup.sh
```

---

## 🎯 Application Flow

**Data Flow:**

- User interacts with Angular UI → Frontend makes API call → Backend queries PostgreSQL → Data returns and displays.

**Example (Article Search):**

- User searches via `DashboardComponent`
- Angular service hits backend API (`/api/v1/articles/`)
- Backend fetches from database
- Results displayed in respective columns

---

## ✅ Complete System Testing

### Using Setup Script

```bash
./setup.sh
cd backend && ./run.sh
cd frontend && ./run.sh
```

### Manual Setup

```bash
# Database
createdb political_content

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
ng serve
```

### Docker

```bash
docker-compose up --build
```

---

## 🚩 Expected Behavior

Running **News Pulse** should yield:

- 🖥️ **Frontend**: Search bar, organized article cards in three columns (left, center, right).
- ⚡ **Backend**: Responsive API providing JSON article data.
- 📦 **Database**: Persistent storage of articles, classifications, and consensus data.

---

🌟 **Enjoy exploring political consensus with News Pulse!** 🌟

# API Testing Guide

## Understanding the Flow

1. **Data Collection Flow**:
   ```
   Your POST request → FastAPI Backend → NewsAPI → Your Database
   ```
   - You send a POST request to collect articles
   - FastAPI receives the request and calls NewsAPI
   - NewsAPI returns the articles
   - FastAPI saves them to your PostgreSQL database

2. **Data Retrieval Flow**:
   ```
   Your GET request → FastAPI Backend → Your Database → Response to You
   ```
   - You send a GET request to view articles
   - FastAPI queries your PostgreSQL database
   - Returns the articles as JSON

## Testing Commands

### 1. Start the Backend Server
```bash
# Terminal 1
cd backend
source venv/bin/activate
./run.sh
```

### 2. Collect Articles (POST Request)

#### Using get_articles_by_topic
```bash
# Terminal 2
# Basic topic search
curl -X POST "http://localhost:8000/api/v1/articles/collect?topic=politics"

# Topic search with language filter (e.g., Spanish articles)
curl -X POST "http://localhost:8000/api/v1/articles/collect?topic=politics&language=es"

# Topic search with date range (last 30 days)
curl -X POST "http://localhost:8000/api/v1/articles/collect?topic=politics&days_back=30"

# Topic search with pagination
curl -X POST "http://localhost:8000/api/v1/articles/collect?topic=politics&page_size=50&page=2"
```

#### Using get_top_headlines
```bash
# Get US political headlines
curl -X POST "http://localhost:8000/api/v1/articles/collect?category=politics&country=us"

# Get headlines from specific category (e.g., business)
curl -X POST "http://localhost:8000/api/v1/articles/collect?category=business"

# Get headlines with pagination
curl -X POST "http://localhost:8000/api/v1/articles/collect?category=politics&page_size=20&page=1"
```

### 3. View Articles (GET Request)
```bash
# Terminal 2 (continued)
# View all articles in the database
curl "http://localhost:8000/api/v1/articles/"

# Filter articles by search term
curl "http://localhost:8000/api/v1/articles/?search=democrat"
curl "http://localhost:8000/api/v1/articles/?search=republican"

# Filter by date range
curl "http://localhost:8000/api/v1/articles/?start_date=2024-01-01&end_date=2024-03-31"

# Filter by source
curl "http://localhost:8000/api/v1/articles/?source=CNN"

# Paginate results
curl "http://localhost:8000/api/v1/articles/?skip=0&limit=100"
```

### 4. Check Database Directly
```bash
# Terminal 3
# Connect to PostgreSQL
psql -U postgres -d political_content

# Basic queries
SELECT COUNT(*) FROM articles;
SELECT title, source_name FROM articles LIMIT 5;

# Advanced analysis
SELECT source_name, COUNT(*) as article_count 
FROM articles 
GROUP BY source_name 
ORDER BY article_count DESC;

SELECT 
    word, 
    COUNT(*) as frequency
FROM (
    SELECT regexp_split_to_table(LOWER(title), '\s+') as word
    FROM articles
) words
WHERE length(word) > 3
GROUP BY word
ORDER BY frequency DESC
LIMIT 20;

# Exit psql
\q
```

## Understanding the Commands



- **POST Requests** (`curl -X POST`): Used to collect new articles because:
  - We're creating new data in the database
  - The operation is not idempotent (multiple calls will create multiple entries)
  - We're changing the state of the system

- **GET Requests** (`curl`): Used to view articles because:
  - We're retrieving existing data
  - The operation is idempotent (multiple calls return the same data)
  - We're not changing the system state

- **Database Queries**: Used to:
  - Verify data is being saved correctly
  - Perform analysis not available through the API
  - Debug and troubleshoot issues

- **Example** ('POST /api/v1/articles/collect'):
  - Curl request hits FastAPI
  - FastAPI calls NewsAPI using NewsClient
  - NewsAPI returns articles
  - FastAPI saves them to db
  - FastAPI returns success msg
- **Example** ('POST /api/v1/articles'): 
  - Your request hits FastAPI
  - FastAPI queries your database
  - Returns the articles stored in your databasea

### psql -U mattsankner -d political_content
   SELECT id, title, source_name FROM articles ORDER BY published_at DESC LIMIT 10;

### Latest 
   python -c "from app.db.session import SessionLocal; from app.models.database import ArticleModel; db = SessionLocal(); articles = db.query(ArticleModel).limit(10).all(); print(f'Total articles: {db.query(ArticleModel).count()}'); [print(f'ID: {a.id}, Title: {a.title}, Source: {a.source_name}') for a in articles]; db.close()"