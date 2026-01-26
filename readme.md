🔐 Agentic RAG-Based Role-Based Access Control (RBAC) Chatbot

This project implements an Agent-driven Retrieval-Augmented Generation (RAG) chatbot with Role-Based Access Control (RBAC) to ensure that every user only accesses data they are authorized to see.

The system authenticates users, assigns roles, intelligently routes each query to the correct pipeline (Vector Search or SQL), retrieves relevant data based on permissions, and generates context-rich, trustworthy responses with source references.

The architecture integrates Redis caching, Hybrid Search (Dense + BM25), RRF fusion, Cohere re-ranking, PostgreSQL, Qdrant vector database, a modular Evaluation-Service (RAGAS), and a Streamlit-based UI, delivering an enterprise-grade, scalable, and production-ready chatbot platform.

Each user query flows through a secure pipeline that combines natural language understanding, agent-based routing, access control, retrieval, ranking, caching, evaluation, and LLM reasoning to deliver accurate, compliant, and low-latency answers.

🧠 System Overview
High-Level Architecture
flowchart LR
    %% Users
    U[Users] -->|Query| UI[Streamlit UI]

    %% UI Layer
    UI --> CACHE[Redis Cache]
    CACHE --> AGENT[Agent Router]

    %% Pipelines
    AGENT --> RAG[Vector Search Pipeline (Qdrant)]
    AGENT --> SQL[SQL Pipeline (PostgreSQL)]

    %% LLM Layer
    RAG --> LLM[LLM Response Engine]
    SQL --> LLM

    %% Output
    LLM --> UI
    LLM --> EVAL[Evaluation Service (RAGAS)]

    %% Deployment
    subgraph DEPLOY[Deployment]
        DOCKER[Docker Containers] --> UI
        DOCKER --> AGENT
        DOCKER --> RAG
        DOCKER --> SQL
        DOCKER --> LLM
        DOCKER --> CACHE
        DOCKER --> EVAL
        RENDER[Render Cloud Hosting] --> DOCKER
    end


👥 Roles & Permissions

Each user is assigned a role that determines what data can be accessed:

Role	Accessible Data
Finance Team	Financial reports, expenses, equipment costs, reimbursements
Marketing Team	Campaign performance, customer feedback, sales metrics
HR Team	Employee data, attendance, payroll, performance reviews
Engineering Department	Architecture, development processes, operational guidelines
C-Level Executives	Full access to all company data
Employee Level	General company information, policies, events, FAQs

Role filters are applied before retrieval, ensuring unauthorized data is never passed to the LLM.

🤖 Agent-Based Tool Routing

The chatbot uses an intelligent Agent to analyze each query and decide which tool to execute:

knowledge_search → Unstructured documents (RAG / Vector DB)

text_to_sql → Structured database queries (PostgreSQL)

The Agent considers:

Query intent

Data type (textual vs numeric)

Aggregations / filters

Role permissions

This ensures queries are processed securely through the correct pipeline.

⚡ Redis Caching Layer

Redis is used as a pre-agent caching layer to store query-response pairs:

Exact cache (identical queries)

Semantic cache (optional, embedding-based)

Role-aware keys to prevent data leakage

Example key:

rbac:{hash({role}|query)}

🔎 Hybrid Search + RRF + Cohere

Hybrid Search: Dense embeddings (Qdrant) + BM25 keyword search

RRF Fusion: Combines Dense & BM25 results for better recall

Cohere Re-Ranking: Optimizes top-K candidates for precision before passing to LLM

🧮 SQL Pipeline (PostgreSQL)

Structured queries use Text-to-SQL with:

Role-based table & column access

Secure, read-only execution

Conversion of results to natural language

🗄️ Qdrant Vector Database

Stores unstructured documents with embeddings

Includes metadata for RBAC filtering

Supports fast, scalable, dense retrieval

🧪 Modular Evaluation Service

Separate background service for RAGAS evaluation

Evaluates responses on faithfulness, relevance, context precision & recall

Modular and reusable across pipelines

Non-blocking for user queries

Results shown on Streamlit Evaluation Dashboard

🖥️ Streamlit UI

Provides:

Chat interface for all users

File upload for knowledge base updates

Evaluation Dashboard for admins

User management for C-Level / Admins

🐳 Deployment

Docker: Full containerization of backend, UI, cache, evaluation, and pipelines

Render: Cloud hosting with auto-scaling and secure environment variables

🚀 Benefits

Secure, role-based access

Agent-based intelligent routing (RAG vs SQL)

Hybrid search + RRF + Cohere re-ranking

Redis caching for performance

Modular Evaluation-Service for continuous monitoring

Streamlit UI for usability and admin control

Docker + Render deployment for production-ready hosting

🏁 Summary

This project combines Agentic AI, RBAC, Redis caching, Hybrid Search (Dense + BM25), RRF fusion, Cohere re-ranking, PostgreSQL, Qdrant vector storage, a modular Evaluation-Service, Streamlit UI, and Docker-based Render deployment to deliver a secure, scalable, and intelligent chatbot platform that:

Dynamically routes queries

Retrieves the right data

Generates context-rich responses with sources

Continuously evaluates system performance

Ensures users see only what they are authorized to see