🛠️ Getting Started

Follow these steps to run the Agentic RBAC RAG Chatbot locally or deploy to the cloud.

1️⃣ Prerequisites

Ensure the following are installed:

Docker

Python 3.10+

Render account (for cloud deployment)

2️⃣ Clone the Repository
git clone https://github.com/your-username/rbac-chatbot.git
cd rbac-chatbot

3️⃣ Environment Variables

Create a .env file in the project root:

# PostgreSQL
POSTGRES_USER=rbac_user
POSTGRES_PASSWORD=rbac_pass
POSTGRES_DB=rbac_db
POSTGRES_HOST=postgres

# Qdrant
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=YOUR_QDRANT_API_KEY

# Redis
REDIS_URL=redis://redis:6379

# LLM / Cohere API
COHERE_API_KEY=YOUR_COHERE_KEY
OPENAI_API_KEY=YOUR_OPENAI_KEY

# Admin Credentials
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=securepassword

4️⃣ Docker Setup

The project includes a docker-compose.yml for all services:

version: '3.8'
services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
  
  qdrant:
    image: qdrant/qdrant:v1.2.2
    ports:
      - "6333:6333"
  
  chatbot:
    build: ./backend
    env_file: .env
    depends_on:
      - redis
      - postgres
      - qdrant
    ports:
      - "8000:8000"
  
  streamlit-ui:
    build: ./ui
    env_file: .env
    ports:
      - "8501:8501"
    depends_on:
      - chatbot


Run all services:

docker-compose up --build


Access services:

Chatbot API: http://localhost:8000

Streamlit UI: http://localhost:8501

Redis: localhost:6379

PostgreSQL: localhost:5432

Qdrant: http://localhost:6333

5️⃣ Streamlit UI

Launch the chatbot interface and admin dashboard:

cd ui
streamlit run app.py


Chat interface for all users

File upload for knowledge base

Evaluation dashboard (RAGAS metrics)

Admin panel for C-level users

6️⃣ Evaluation Service (Background Task)

The Evaluation-Service runs asynchronously to evaluate responses using RAGAS:

cd evaluation_service
python main.py


Can run on a separate container or VM

Periodically fetches chatbot responses

Computes faithfulness, relevance, context precision & recall

Updates evaluation dashboard

7️⃣ Initial User Setup

Default admin user (C-level) can be created via .env credentials

Admin can add new users and assign roles via Streamlit UI

8️⃣ Deployment on Render

Push the repo to GitHub.

Create a Render web service for the chatbot:

Environment: Docker

Ports: 8000 (API), 8501 (UI)

Configure Redis, Postgres, and Qdrant as separate Render services or managed cloud instances.

Add environment variables in Render dashboard from .env.

Deploy — Render handles auto-scaling and HTTPS.

9️⃣ Notes

Redis caching improves performance by storing query responses.

Hybrid Search + RRF + Cohere Re-Ranking ensures high-quality, context-aware answers.

Modular Evaluation-Service ensures metrics are computed asynchronously and can be reused across multiple pipelines.

✅ After setup, users can:

Query the chatbot according to their role

Upload new documents for the knowledge base

Monitor evaluation metrics

Admins can manage users, roles, and system configuration