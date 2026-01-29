"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI Configuration
    # openai_api_key: str

    # Google Configuration
    google_api_key: str

    # Qdrant Cloud Configuration
    qdrant_url: str
    qdrant_api_key: str


    # Collection Settings
    collection_name: str = "RBAC_CHATBOT"

    # Document Processing Settings
    chunk_size: int = 420
    chunk_overlap: int = int(chunk_size*0.1)

    # Model Configuration
    embedding_model: str = "gemini-embedding-001"
    llm_model: str = "gemini-2.5-flash"
    llm_provider: str = "vertex"

    llm_temperature: float = 0.0

    # Retrieval Settings
    top_k: int = 15
    sparse_retriever_type:str = "BM25"
    alpha:float = 0.80

    # Logging
    log_level: str = "INFO"


    # API Settings
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    # streamlit 
    ui_port: str = "8002"

    # Application Info
    app_name: str = "rbac_chatbot"
    app_version: str = "0.1.0"

    # Database Settings
    qdrant_path:str = "./resources/data/qdrant_db_latest/rbac_chatbot.db"

    #JWT Config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Evaluation Service
    evaluation_service_url:str

    # Postgress server path
    database_url:str

    # DB Schema
    db_schema_path:str


    # Redis
    ENABLE_CACHE:bool
    REDIS_REST_URL:str
    REDIS_REST_TOKEN:str
    CACHE_TTL_RAG: int = 3600

    # Reranking
    ENABLE_RERANKING:bool
    COHERE_API_KEY:str
    COHERE_TOP_N:int
    RERANK_MODEL:str

    #Enviornment
    env:str="dev"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
