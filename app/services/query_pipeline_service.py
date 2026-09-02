"""Helpers for the main query-processing workflow."""

import json

from app.config.config import get_settings
from app.services.chat_service import ChatService
from app.services.query_cache_service import QueryCacheService
from app.utils.langfuse_tracing import build_langchain_config, trace_cache_hit
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


async def execute_query_pipeline(question: str, user_info: dict) -> tuple[str, list, dict | None, dict | None]:
    """Execute the query flow and return answer plus source metadata."""
    chat_service = ChatService(user_info=user_info)
    query_cache_service = QueryCacheService(
        redis_url=settings.REDIS_REST_URL,
        redis_token=settings.REDIS_REST_TOKEN,
    )

    if query_cache_service and query_cache_service.enabled:
        roles = [str(role).strip().lower() for role in (user_info.get("roles") or ["general"]) if str(role).strip()]
        main_role = roles[0] if roles else "general"
        allowed_roles = roles if roles else ["general"]
        cache_keys = query_cache_service.get_lookup_keys(question, role=main_role, allowed_roles=allowed_roles)

        cached_result = None
        for cache_key in cache_keys:
            cached_result = query_cache_service.get(cache_key, cache_type="rag")
            if cached_result:
                logger.info(f"Cache HIT {cache_key} for question: '{question[:50]}...'")
                trace_cache_hit(
                    user_info=user_info,
                    question=question,
                    cache_key=cache_key,
                    cache_type="rag",
                )
                answer = cached_result.get("answer", "")
                sources = cached_result.get("sources", [])
                return answer, sources, None, None
    else:
        cache_keys = []

    result = await chat_service.chat(
        question=question,
        conversation_id=user_info["conversation_id"],
    )

    answer = result.get("answer", "")
    knowledgge_base_resp = result.get("knowledgge_base_resp")
    text_to_sql_resp = result.get("text_to_sql_resp")

    sources: list = []
    if knowledgge_base_resp and knowledgge_base_resp.get('status') != 'ACCESS_DENIED' and knowledgge_base_resp.get("sources") is not None:
        try:
            sources = json.loads(knowledgge_base_resp["sources"])
        except (TypeError, ValueError):
            sources = knowledgge_base_resp.get("sources", [])

    if text_to_sql_resp and text_to_sql_resp.get("results") is not None:
        sources.append({"page_content": text_to_sql_resp.get("results")})

    if query_cache_service and query_cache_service.enabled:
        cache_result = {
            "question": question,
            "answer": answer,
            "sources": sources,
        }

        if knowledgge_base_resp:
            cache_result["chunks_used"] = len(sources)
            cache_result["model"] = settings.llm_model
            cache_result["tool"] = knowledgge_base_resp.get("tool")

        if text_to_sql_resp:
            cache_result["sql_query"] = text_to_sql_resp.get("sql_query")
            cache_result["sql_result"] = text_to_sql_resp.get("results")
            cache_result["row_count"] = text_to_sql_resp.get("row_count")

        ttl = settings.CACHE_TTL_RAG
        if knowledgge_base_resp.get('status') != 'ACCESS_DENIED':
            for cache_key in dict.fromkeys([query_cache_service.get_key(question, (roles[0] if roles else "general"))]):
                query_cache_service.set(cache_key, cache_result, ttl=ttl, cache_type="rag")

    return answer, sources, knowledgge_base_resp, text_to_sql_resp
