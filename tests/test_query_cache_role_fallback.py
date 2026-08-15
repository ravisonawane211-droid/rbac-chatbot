from app.services.query_cache_service import QueryCacheService


def test_general_cache_is_used_as_fallback_for_specific_roles():
    service = QueryCacheService()
    question = "What is the leave policy?"

    cache_keys = service.get_lookup_keys(question, "marketing")

    assert cache_keys[0] == service.get_key(question, "marketing")
    assert cache_keys[1] == service.get_key(question, "general")
    assert len(cache_keys) == 2
