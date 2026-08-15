import re
from typing import Any, Dict

import sqlglot

from app.utils.logger import get_logger


class SQLValidationSerice:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("SQLValidationSerice initialized")

    def validate_sql_query(
        self,
        sql_query: str,
        schema_component: Dict[str, Any] | None = None,
        allowed_tables: list | None = None,
        user_info: dict | None = None,
    ):
        try:
            self.logger.info("Starting SQL query validation")

            self._validate_against_role(sql_query=sql_query, allowed_tables=allowed_tables or [])
            self._validate_basic_syntax(sql_query=sql_query)
            self._validate_against_schema(
                sql_query=sql_query,
                schema_component=schema_component or {"schema": []},
            )

            self.logger.info("SQL query validation successful.")
        except Exception as e:
            self.logger.error(f"Error while validating sql query {e}")
            raise

    def _validate_against_role(self, sql_query: str, allowed_tables: list | None = None):
        self.logger.info("Validating role to access tables in query")

        if self._validate_tables(sql_query=sql_query, allowed_tables=allowed_tables or [], alias_map={}):
            raise Exception("Your role does not allow access to the data needed for this request.")

        self.logger.info("Validating role to access tables in query completed")

    def _validate_basic_syntax(self, sql_query: str):
        self.logger.info("Validating basic syntax of query")

        if self._validate_structure(sql_query=sql_query):
            raise Exception(
                "SQL query validation failed due to syntax error in query. Please verify generated query."
            )

        if self._validate_security(sql_query=sql_query):
            raise Exception(
                "SQL query validation failed due to unsafe database operation. Please verify generated query."
            )

    def _validate_against_schema(self, sql_query: str, schema_component: Dict[str, Any] | None = None):
        self.logger.info("Validating SQL query against schema")

        tables = (schema_component or {}).get("schema", [])
        valid_tables = [table.get("table_name", "") for table in tables]
        schema_map = {table.get("table_name"): table.get("columns", []) for table in tables}
        alias_map = {}

        if self._validate_tables(sql_query=sql_query, allowed_tables=valid_tables, alias_map=alias_map):
            raise Exception(
                "SQL query validation failed due to invalid table in query. Please verify generated query."
            )

        if self._validate_columns(sql_query=sql_query, schema_map=schema_map, alias_map=alias_map):
            raise Exception(
                "SQL query validation failed due to invalid column in query. Please verify generated query."
            )

    def _validate_structure(self, sql_query: str):
        self.logger.info("Validating SQL query structure")

        s = sql_query.strip().lower()
        if not s.startswith(("select", "with")):
            return True

        if s.count(";") > 1:
            return True

        return False

    def _validate_security(self, sql_query: str):
        self.logger.info("Validating database safe operation in SQL query")

        blocked = r"\b(insert|update|delete|drop|alter|truncate|merge|create|grant|revoke)\b"
        return bool(re.search(blocked, sql_query, re.IGNORECASE))

    def _validate_tables(self, sql_query: str, allowed_tables: list, alias_map: dict):
        self.logger.info("Validating valid tables in SQL query")
        parsed = sqlglot.parse_one(sql_query)
        cte_names = {cte.alias_or_name.lower() for cte in parsed.find_all(sqlglot.exp.CTE)}

        for table in parsed.find_all(sqlglot.exp.Table):
            table_name = table.name
            if not table_name:
                continue

            if table_name.lower() in cte_names:
                continue

            alias = table.alias_or_name
            alias_map[alias] = table.this
            if table_name not in allowed_tables:
                return True
        return False

    def _validate_columns(self, sql_query, schema_map: Dict[str, Any], alias_map: dict):
        self.logger.info("Validating valid columns in SQL query")

        parsed = sqlglot.parse_one(sql_query)
        cte_columns = {}
        for cte in parsed.find_all(sqlglot.exp.CTE):
            cte_name = cte.alias_or_name.lower()
            column_names = []
            for select in cte.this.selects:
                selected_name = (
                    select.alias_or_name
                    or getattr(getattr(select, "this", None), "name", None)
                    or getattr(select, "name", None)
                )
                if selected_name:
                    column_names.append(selected_name)
            cte_columns[cte_name] = column_names

        known_columns = set()
        for table_columns in schema_map.values():
            known_columns.update(
                column.get("name")
                for column in table_columns
                if isinstance(column, dict) and column.get("name")
            )
        for columns in cte_columns.values():
            known_columns.update(columns)

        for col in parsed.find_all(sqlglot.exp.Column):
            alias = col.table
            name = col.name

            if alias:
                alias_entry = alias_map.get(alias)
                if alias_entry is not None:
                    table_real = getattr(alias_entry, "name", None)
                else:
                    table_real = alias if alias in schema_map else None

                if alias_entry is None and table_real is None:
                    cte_name = alias.lower() if isinstance(alias, str) else None
                    if cte_name in cte_columns and name in cte_columns[cte_name]:
                        continue
                    continue
            else:
                table_real = None
                if name in known_columns:
                    continue

            if table_real is not None:
                column_list = [
                    column.get("name")
                    for column in schema_map.get(table_real, [])
                    if isinstance(column, dict)
                ]
                if name not in column_list:
                    raise ValueError(f"Invalid column {alias}.{name}")
            elif name not in known_columns:
                raise ValueError(f"Invalid column {alias}.{name}")

        return False
