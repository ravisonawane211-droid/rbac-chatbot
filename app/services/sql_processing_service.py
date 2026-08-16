import json
import sys
from pathlib import Path
from typing import Any, Dict

from app.config.config import get_settings
from app.services.db_execute_service import DatabaseExecuteService
from app.services.sql_access_service import get_allowed_tables_for_roles
from app.services.sql_generation_service import SQLGenerationService
from app.services.sql_validation_service import SQLValidationSerice
from app.utils.logger import get_logger

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

settings = get_settings()


class SQLProcessingService:
    def __init__(self, user_query: str, format_answer: bool = True, user_info: dict | None = None) -> None:
        self.logger = get_logger(__name__)
        self.user_info = user_info or {}
        self.roles = self.user_info.get("roles", [])
        self.format_answer = format_answer
        self.user_query = user_query
        self.db_schema_path = settings.db_schema_path
        self.sql_query = ""

        self.sql_generation_service = SQLGenerationService()
        self.sql_validation_service = SQLValidationSerice()
        self.db_executor = DatabaseExecuteService(db_config=settings.database_url)

        self.logger.info("SQLProcessingService initialized")

    def process_user_query(self) -> Dict[str, Any]:
        try:
            self.logger.info("SQL query processing started")

            schema_components = self._process_db_schema(db_schema_path=self.db_schema_path)
            self.sql_query = self.sql_generation_service.generate_sql_query(
                user_query=self.user_query,
                entities=None,
                schema_components=schema_components,
                user_info=self.user_info,
            )

            allowed_tables = self._get_allowed_tables_for_user()
            self.sql_validation_service.validate_sql_query(
                sql_query=self.sql_query,
                schema_component=schema_components,
                allowed_tables=allowed_tables,
                user_info=self.user_info,
            )

            result_df = self.db_executor.execute_sql_query(sql_query=self.sql_query)
            self.logger.info(f"User Query process and result : {result_df}")

            result = {
                "status": "success",
                "sql_query": self.sql_query,
                "results": result_df.to_json(date_format="iso", orient="records"),
                "row_count": len(result_df),
            }
            return result

        except Exception as e:
            self.logger.error(f"SQL Query processing failed: {e}")
            result = {
                "status": "Failed",
                "sql_query": self.sql_query,
                "results": [],
                "row_count": 0,
                "message": "Error while procesing user query",
                "error": str(e),
            }
            return result

    def _get_allowed_tables_for_user(self) -> list[str]:
        return get_allowed_tables_for_roles(self.db_executor, self.roles)

    # app/services/sql_processing_service.py

    def _process_db_schema(self, db_schema_path: str = settings.db_schema_path):
        schema_path = Path(db_schema_path)

        if not schema_path.is_absolute():
            schema_path = project_root / schema_path

        with schema_path.open("r", encoding="utf-8") as file:
            return json.load(file)


if __name__ == "__main__":
    sql_processing_service = SQLProcessingService(user_query="Employee count in Finsolve Technologies")
    result = sql_processing_service.process_user_query()
    print(f"User Query: {sql_processing_service.user_query}")
    print(f"SQL query: {sql_processing_service.sql_query}")
    print(f"Result: {result}")

