"""Langfuse tracing helpers for LangChain and app-level observability."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Mapping

from app.config.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def build_langfuse_metadata(
    user_info: Mapping[str, Any] | None = None,
    route: str | None = None,
    model: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """Build metadata payload for LangChain traces."""
    user_info = user_info or {}
    roles = user_info.get("roles") or []
    if isinstance(roles, str):
        roles = [roles]

    metadata: dict[str, Any] = {
        "langfuse_user_id": user_info.get("user_id") or user_info.get("sub") or user_info.get("email"),
        "langfuse_session_id": user_info.get("conversation_id") or user_info.get("session_id"),
        "langfuse_tags": [str(role) for role in roles if role],
    }

    if route:
        metadata["route"] = route
    if model:
        metadata["model"] = model

    for key, value in extra.items():
        if value not in (None, "", [], {}):
            metadata[key] = value

    return {key: value for key, value in metadata.items() if value not in (None, "", [], {})}


def build_langchain_config(
    user_info: Mapping[str, Any] | None = None,
    route: str | None = None,
    model: str | None = None,
    base_config: dict[str, Any] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """Return LangChain invoke config with Langfuse callback and metadata."""
    config = dict(base_config or {})
    langfuse_handler = get_langfuse_handler()
    if langfuse_handler:
        config["callbacks"] = [langfuse_handler]
    metadata = build_langfuse_metadata(user_info=user_info, route=route, model=model, **extra)
    if metadata:
        config["metadata"] = metadata
    return config


def trace_cache_hit(
    user_info: Mapping[str, Any] | None = None,
    question: str | None = None,
    cache_key: str | None = None,
    cache_type: str = "rag",
) -> Any | None:
    """Emit a Langfuse event when a cached answer is reused."""
    langfuse_handler = get_langfuse_handler()
    if not langfuse_handler:
        return None

    try:
        from langfuse import get_client

        client = get_client()
        trace_context = None
        current_trace_id = client.get_current_trace_id()
        if current_trace_id:
            trace_context = {"id": current_trace_id}

        return client.create_event(
            trace_context=trace_context,
            name="cache_hit",
            input={
                "question": question,
                "cache_key": cache_key,
                "cache_type": cache_type,
                "user": user_info,
            },
            output={"status": "served_from_cache"},
            metadata={
                "cache_key": cache_key,
                "cache_type": cache_type,
                **build_langfuse_metadata(user_info=user_info, route="/cache-hit"),
            },
            level="DEFAULT",
        )
    except Exception as exc:  # pragma: no cover - defensive fallback
        logger.warning("Langfuse cache-hit trace unavailable: %s", exc)
        return None


@lru_cache(maxsize=1)
def get_langfuse_handler():
    """Return a LangChain callback handler when Langfuse is configured."""
    refreshed_settings = get_settings()

    public_key = os.getenv("LANGFUSE_PUBLIC_KEY") or refreshed_settings.langfuse_public_key
    secret_key = os.getenv("LANGFUSE_SECRET_KEY") or refreshed_settings.langfuse_secret_key
    base_url = os.getenv("LANGFUSE_BASE_URL") or refreshed_settings.langfuse_base_url

    if not public_key or not secret_key:
        logger.info("Langfuse tracing disabled: missing LANGFUSE_PUBLIC_KEY or LANGFUSE_SECRET_KEY")
        return None

    try:
        from langfuse import get_client
        from langfuse.langchain import CallbackHandler

        if base_url:
            os.environ.setdefault("LANGFUSE_BASE_URL", base_url)

        langfuse = get_client()
        if not getattr(langfuse, "auth_check", lambda: False)():
            logger.warning("Langfuse tracing disabled: credentials are not authenticated")
            return None

        return CallbackHandler()
    except Exception as exc:  # pragma: no cover - defensive fallback
        logger.warning("Langfuse handlers unavailable: %s", exc)
        return None
