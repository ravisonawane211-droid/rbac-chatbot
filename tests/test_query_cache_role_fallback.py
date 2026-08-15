from app.services.query_cache_service import QueryCacheService


def test_role_specific_cache_is_not_shared_with_other_roles():
    service = QueryCacheService()
    question = "What is the leave policy?"

    cache_keys = service.get_lookup_keys(question, "marketing")

    assert cache_keys == [service.get_key(question, "marketing")]


def test_c_level_can_access_shared_role_cache():
    service = QueryCacheService()
    question = "What is the leave policy?"

    cache_keys = service.get_lookup_keys(question, "c-level")

    assert service.get_key(question, "c-level") in cache_keys
    assert service.get_key(question, "general") in cache_keys
    assert service.get_key(question, "marketing") in cache_keys
