"""Helpers for role-based SQL table access checks."""

from collections.abc import Iterable


def build_role_filter(roles: Iterable[str]) -> str:
    """Return a SQL-safe IN clause for a role set."""
    normalized_roles = {role.strip() for role in roles if role and str(role).strip()}
    if not normalized_roles:
        normalized_roles = {"general"}

    return ",".join(f"'{role}'" for role in sorted(normalized_roles))


def get_allowed_tables_for_roles(db_executor, roles: Iterable[str]) -> list[str]:
    """Resolve all tables permitted for the provided role set."""
    role_names = set(roles)
    role_names.add("general")

    role_filter = build_role_filter(role_names)
    query = f"SELECT table_name FROM table_access_roles WHERE ROLE_NAME IN ({role_filter})"

    access_tables = db_executor.execute_sql_query(sql_query=query)
    if access_tables is None or access_tables.empty:
        return []

    return access_tables["table_name"].tolist()
