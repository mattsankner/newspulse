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

