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

    google_api_key: str
    openai_api_key: str

    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_base_url: str | None = None

    collection_name: str = "RBAC_CHATBOT"

    chunk_size: int = 420
    chunk_overlap: int = 42

    embedding_model: str = "gemini-embedding-001"
    llm_model: str = "gpt-5-mini"
    llm_provider: str = "openai"
    llm_temperature: float = 0.0

    top_k: int = 15
    sparse_retriever_type: str = "BM25"
    alpha: float = 0.80

    log_level: str = "INFO"

    api_host: str = "127.0.0.1"
    api_port: int = 8000
    ui_port: str = "8002"

    app_name: str = "rbac_chatbot"
    app_version: str = "0.1.0"

    qdrant_path: str = "./resources/data/qdrant_db_latest/rbac_chatbot.db"

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    enable_evaluation: bool
    evaluation_service_url: str
    eval_type: str

    database_url: str
    db_schema_path: str

    ENABLE_CACHE: bool
    REDIS_REST_URL: str
    REDIS_REST_TOKEN: str
    CACHE_TTL_RAG: int = 86400

    ENABLE_RERANKING: bool
    COHERE_API_KEY: str
    COHERE_TOP_N: int
    RERANK_MODEL: str

    CHATBOT_SERVICE_URL: str

    env: str = "dev"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
