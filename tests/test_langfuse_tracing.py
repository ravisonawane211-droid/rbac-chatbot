import os


def test_build_langfuse_metadata_includes_user_and_session():
    from app.utils.langfuse_tracing import build_langfuse_metadata

    metadata = build_langfuse_metadata(
        user_info={
            "user_id": "user-123",
            "conversation_id": "session-456",
            "roles": ["admin", "finance"],
        },
        route="/query",
        model="gpt-5-mini",
    )

    assert metadata["langfuse_user_id"] == "user-123"
    assert metadata["langfuse_session_id"] == "session-456"
    assert metadata["langfuse_tags"] == ["admin", "finance"]
    assert metadata["route"] == "/query"
    assert metadata["model"] == "gpt-5-mini"


def test_get_langfuse_handler_returns_none_without_credentials(monkeypatch):
    from app.utils.langfuse_tracing import get_langfuse_handler

    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_BASE_URL", raising=False)

    assert get_langfuse_handler() is None


def test_build_langchain_config_adds_callback_and_metadata(monkeypatch):
    from app.utils.langfuse_tracing import build_langchain_config

    class FakeHandler:
        pass

    monkeypatch.setattr(
        "app.utils.langfuse_tracing.get_langfuse_handler",
        lambda: FakeHandler(),
    )

    config = build_langchain_config(
        user_info={"user_id": "user-123", "conversation_id": "session-456", "roles": ["admin"]},
        route="/query",
        model="gpt-5-mini",
        base_config={"configurable": {"thread_id": "conv-1"}},
    )

    assert config["configurable"]["thread_id"] == "conv-1"
    assert config["metadata"]["langfuse_user_id"] == "user-123"
    assert config["metadata"]["langfuse_session_id"] == "session-456"
    assert len(config["callbacks"]) == 1


def test_trace_cache_hit_includes_latency_cost_and_flow(monkeypatch):
    from app.utils.langfuse_tracing import trace_cache_hit

    class FakeClient:
        def get_current_trace_id(self):
            return "trace-123"

        def create_event(self, **kwargs):
            return {"metadata": kwargs["metadata"], "input": kwargs["input"], "output": kwargs["output"]}

    monkeypatch.setattr("app.utils.langfuse_tracing.get_langfuse_handler", lambda: object())
    monkeypatch.setattr("langfuse.get_client", lambda: FakeClient())

    result = trace_cache_hit(
        user_info={"user_id": "user-123", "conversation_id": "session-456", "roles": ["finance"]},
        question="what is our hiring policy?",
        cache_key="finance:abc123",
        cache_type="rag",
        latency_ms=123,
        estimated_cost=0.0,
        request_flow="query->cache->response",
    )

    assert result["metadata"]["latency_ms"] == 123
    assert result["metadata"]["estimated_cost"] == 0.0
    assert result["metadata"]["request_flow"] == "query->cache->response"
    assert result["output"]["status"] == "served_from_cache"


def test_validate_sql_query_allows_cte_aliases():
    from app.services.sql_validation_service import SQLValidationSerice

    sql = '''
    WITH mgr AS (
        SELECT manager_id FROM employee WHERE employee_id = 'FINEMP1055'
    ),
    peers AS (
        SELECT e.employee_id, e.full_name, e.role, d.department_name, e.email
        FROM employee e
        INNER JOIN departments d ON e.department_id = d.department_id
        WHERE e.manager_id = (SELECT manager_id FROM mgr)
        AND e.employee_id <> 'FINEMP1055'
    )
    SELECT employee_id, full_name, role, department_name, email
    FROM peers
    UNION ALL
    SELECT NULL::varchar(20) AS employee_id,
    CASE
        WHEN (SELECT COUNT(*) FROM mgr) = 0 THEN 'Employee FINEMP1055 not found.'
        WHEN (SELECT manager_id FROM mgr) IS NULL THEN 'Employee FINEMP1055 has no manager assigned.'
        ELSE 'No other employees report to manager ' || (SELECT manager_id FROM mgr)
    END AS full_name,
    NULL::varchar(100) AS role,
    NULL::varchar(100) AS department_name,
    NULL::varchar(150) AS email
    WHERE NOT EXISTS (SELECT 1 FROM peers)
    ORDER BY full_name NULLS LAST
    LIMIT 100;
    '''

    validator = SQLValidationSerice()
    schema = {
        "schema": [
            {"table_name": "employee", "columns": [{"name": "employee_id"}, {"name": "manager_id"}, {"name": "department_id"}, {"name": "full_name"}, {"name": "role"}, {"name": "email"}]},
            {"table_name": "departments", "columns": [{"name": "department_id"}, {"name": "department_name"}]},
        ]
    }

    validator.validate_sql_query(
        sql_query=sql,
        schema_component=schema,
        allowed_tables=["employee", "departments"],
        user_info={"roles": ["finance"]},
    )


def test_validate_sql_query_with_real_schema_shape_does_not_crash():
    from app.services.sql_validation_service import SQLValidationSerice

    validator = SQLValidationSerice()
    schema = {
        "schema": [
            {
                "table_name": "employee",
                "columns": [
                    {"name": "employee_id"},
                    {"name": "full_name"},
                    {"name": "manager_id"},
                ],
            }
        ]
    }

    validator.validate_sql_query(
        sql_query="SELECT e.full_name FROM employee e WHERE e.employee_id = 'FINEMP1055' LIMIT 100;",
        schema_component=schema,
        allowed_tables=["employee"],
        user_info={"roles": ["finance"]},
    )


def test_database_execute_service_reuses_single_engine():
    from app.services.db_execute_service import DatabaseExecuteService, get_shared_engine

    service_a = DatabaseExecuteService(db_config="postgresql://user:pass@localhost:5432/testdb")
    service_b = DatabaseExecuteService(db_config="postgresql://user:pass@localhost:5432/testdb")

    assert service_a.engine is service_b.engine
    assert service_a.engine is get_shared_engine("postgresql://user:pass@localhost:5432/testdb")
