# 🔐 Agentic RAG-Based Role-Based Access Control (RBAC) Chatbot

This project implements an **Agent-driven Retrieval-Augmented Generation (RAG)** chatbot with ***Role-Based Access Control (RBAC)*** to ensure that every user only accesses data they are authorized to see.

The system authenticates users, assigns roles, intelligently routes each query to the correct pipeline (Vector Search or SQL), retrieves relevant data based on permissions, and generates context-rich, trustworthy responses with source references.

The architecture integrates Redis caching, Hybrid Search (Dense + BM25), RRF fusion, Cohere re-ranking, PostgreSQL, Qdrant vector database, a modular ***Evaluation-Service (RAGAS/LLM-As-Judge)***, and a Streamlit-based UI, delivering an enterprise-grade, scalable, and production-ready chatbot platform.

Each user query flows through a secure pipeline that combines natural language understanding, agent-based routing, access control, retrieval, ranking, caching, evaluation, and LLM reasoning to deliver accurate, compliant, and low-latency answers.

## 🧠 System Overview
```
User Login to Chatbot
   ↓  
Authentication & Role Validation
   ↓
User Query
   ↓
Query Validation(Prompt Injection Detection , Normalization)
   ↓  
Redis Cache Check  
   ↓  
Agent-Based Query Routing  
   ↓  
 ┌──────────────────────────┬─────────────────────────┐  
 │ Vector Search (RAG)      │   SQL Pipeline          │  
 │ Hybrid: Dense + BM25     │   Text-to-SQL (Postgres)|
 │                          |   SQL Query Validation  |
 |                          |   Query Execution       |
 │ + Keyword Index +        │                         │  
 | RRF + Cohere Re-Ranking  |                         | 
 | + Role-Based             |                         |
 | Filtering                |                         |                        
 ┴──────────────────────────┴─────────────────────────┘  
   ↓  
Context Augmentation  
   ↓  
LLM Response Generation  
   ↓  
Answer with Source References  
   ↓  
Evaluation-Service (RAGAS) – Background / Asynchronous
```

### 👥 Roles & Permissions

Each user is assigned a role that determines what data can be accessed:


| Role                   | Accessible Data                                                                 |
|------------------------|----------------------------------------------------------------------------------|
| Finance Team           | Financial reports, expenses, equipment costs, reimbursements                     |
| Marketing Team         | Campaign performance, customer feedback, sales metrics                           |
| HR Team                | Employee data, attendance, payroll, performance reviews                          |
| Engineering Department | Architecture, development processes, operational guidelines                      |
| C-Level Executives     | Full access to all company data                                                   |
| Employee Level         | General company information, policies, events, FAQs                               |


### 🤖 Agent-Based Tool Routing

The chatbot uses an intelligent Agent to analyze each query and decide which tool to execute:

knowledge_search → Unstructured documents (RAG / Vector DB)

text_to_sql → Structured database queries (PostgreSQL)

The Agent considers:

* Query intent

* Data type (textual vs numeric)

* Aggregations / filters

* Role permissions

This ensures queries are processed securely through the correct pipeline.

### ⚡ Redis Caching Layer

Redis is used as a pre-agent caching layer to store query-response pairs:

* Exact cache (identical queries)

* Semantic cache (optional, embedding-based)

* Role-aware keys to prevent data leakage

Example key:

rbac:{hash({role}|query)}

### 🔎 Hybrid Search + RRF + Cohere

***Hybrid Search***: Dense embeddings (Qdrant) + BM25 keyword search

***RRF Fusion***: Combines Dense & BM25 results for better recall

***Cohere Re-Ranking***: Optimizes top-K candidates for precision before passing to LLM

### 🧮 SQL Pipeline (PostgreSQL)

Structured queries use Text-to-SQL with:

* Role-based table & column access

* Query Validation

* Secure, read-only execution

* Conversion of results to natural language

### 🗄️ Qdrant Vector Database

* Stores unstructured documents with embeddings

* Includes metadata for RBAC filtering

* Supports fast, scalable, dense retrieval

### 🧪 Modular Evaluation Service

* Separate background service for RAGAS evaluation

* Evaluates responses on faithfulness, relevance, context precision & recall

* Modular and reusable across pipelines

* Non-blocking for user queries

* Results shown on Streamlit Evaluation Dashboard

### 🖥️ Streamlit UI

Provides:

Chat interface for all users

File upload for knowledge base updates

Evaluation Dashboard for admins

User management for C-Level / Admins

### 🐳 Deployment

Docker: Full containerization of backend, UI, cache, evaluation, and pipelines

Render: Cloud hosting with auto-scaling and secure environment variables

## 🚀 Benefits

Secure, role-based access

Agent-based intelligent routing (RAG vs SQL)

Hybrid search + RRF + Cohere re-ranking

Redis caching for performance

Modular Evaluation-Service for continuous monitoring

Streamlit UI for usability and admin control

Docker + Render deployment for production-ready hosting



## 🛠️ API Endpoints

The RBAC RAG Chatbot backend is built with FastAPI and exposes endpoints for user management, document ingestion, query handling, dashboard metrics, and health checks.

All endpoints requiring authentication use JWT Bearer tokens.

### 1️⃣ Health Checks
***GET /health***

Basic health check of the service.

***Response***:
```
{
  "status": "ok",
  "version": "0.1.0",
  "timestamp": "2026-01-26T12:34:56Z"
}
```
***GET /health/ready***

Readiness check including DB and Qdrant connectivity.

***Response***:
```
{
  "status": "ready",
  "qdrant_connected": true,
  "collection_info": { "documents_count": 123 }
}
```

### 2️⃣ Users
***POST /users/login***

Authenticate a user and return a JWT token.

***Request Body***:
```
{
  "user_name": "john.doe",
  "password": "securepassword"
}
```

***Response***:
```
{
  "access_token": "jwt_token_here",
  "role": ["finance"]
}
```
***POST /users***

Create a new user (admin only).

***Request Body***:
```
{
  "user": {
    "user_id": "jane.doe",
    "email": "jane@example.com",
    "user_role": ["hr"]
  },
  "created_by": "admin_user"
}
```

***Response***:
```
{
  "message": "User created successfully"
}
```
### 3️⃣ Documents
***POST /documents/upload***

Upload a document (PDF, TXT, CSV) to the knowledge base.

***Query Parameter***:
```
role – User role for RBAC filtering.
```

***Request Body***: (multipart/form-data)
```
file: report.pdf
```

***Response***:
```
{
  "message": "File uploaded successfully",
  "filename": "report.pdf",
  "chunks_created": 10,
  "document_ids": ["doc_123", "doc_124"]
}
```
***DELETE /documents/collection***

Delete all documents in the vector store (admin only).

***Response***:
```
{ "message": "Collection deleted successfully" }
```
### 4️⃣ Query / Chat
***POST /query***

Submit a question and get an AI-generated answer.

***Request Body***:
```
{
  "question": "What were marketing expenses last quarter?",
  "conversation_id": "abc123",
  "include_sources": true,
  "enable_evaluation": false,
  "user_name": "john.doe"
}
```

***Response***:
```
{
  "question": "What were marketing expenses last quarter?",
  "answer": "Marketing expenses totaled $250,000 in Q4.",
  "sources": [
    {"title": "marketing_q4.pdf", "snippet": "...", "url": "..."}
  ],
  "processing_time_ms": 1200
}
```
***POST /query/stream***

Submit a question and receive a streaming AI response in real-time.

Same request format as /query

Useful for long answers

### 5️⃣ Dashboard
***GET /dashboard/metrics/{app_name}***

Retrieve evaluation and RAG metrics for a specific application.

***Path Parameter***:
```
app_name – Name of the application
```

***Response***:
```
{
  "metrics": [
    {
      "project_id": "proj_123",
      "environment": "prod",
      "question": "What is RAG?",
      "answer": "Retrieval-Augmented Generation is ...",
      "metric_name": "relevance",
      "metric_value": 0.95,
      "eval_status": "completed"
    }
  ],
  "threshold": { "relevance": 0.9 },
  "status": "success"
}
```
***POST /dashboard/config***

Save or update application configuration.

***Request Body***:
```
{
  "user_id": "admin_user",
  "app_config": {
    "enable_eval": "Yes",
    "eval_type": "Ragas"
  }
}
```


***Response***:
```
{
  "status": "success",
  "message": "Configuration saved successfully"
}
```
### 6️⃣ Root UI
***GET /***

Serve the main app.


## 🔑 Security

All protected endpoints require JWT tokens:

Authorization: Bearer <jwt_token>


Role-based access ensures that users only access documents and queries allowed for their role.

## 🏁 Summary

This project combines Agentic AI, RBAC, Redis caching, Hybrid Search (Dense + BM25), RRF fusion, Cohere re-ranking, PostgreSQL, Qdrant vector storage, a modular Evaluation-Service, Streamlit UI, and Docker-based Render deployment to deliver a secure, scalable, and intelligent chatbot platform that:

* **Dynamically routes queries**

* ***Retrieves the right data***

* ***Generates context-rich responses with sources***

* ***Continuously evaluates system performance***

* ***Ensures users see only what they are authorized to see***