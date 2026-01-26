import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.config.config import get_settings
from app.utils.logger import get_logger
from app.services.db_execute_service import DatabaseExecuteService
from app.services.sql_generation_service import SQLGenerationService
from app.services.sql_validation_service import SQLValidationSerice
from app.utils.logger import get_logger
from app.config.config import get_settings
import json
from typing import Dict, Any, List

settings = get_settings()

class SQLProcessingService:

    def __init__(self, user_query:str, format_answer:bool = True, roles: List[str] = []):
        
        self.logger = get_logger(__name__)

        self.roles = roles
        
        self.max_retries = 3
        self.format_answer = format_answer
        self.user_query = user_query
        self.db_schema_path = settings.db_schema_path

        #initialize service classes

        self.sql_generation_service = SQLGenerationService()
        self.sql_validation_service = SQLValidationSerice()
        
        self.db_executor = DatabaseExecuteService()

        self.logger.info("SQLProcessingService Initialized")

    
    def process_user_query(self) -> Dict[str,Any]:

        try:
            self.logger.info("SQL query processing started")

            # 1. Process Schema Info
            schema_components = self._process_db_schema(db_schema_path=self.db_schema_path)

            # 2. Generate SQL using SQL Generation Service

            self.sql_query = self.sql_generation_service.generate_sql_query(user_query=self.user_query , entities=None, 
                                                            schema_components=schema_components)

            # 3. Validate SQL Query using SQL Validation Service

            self.sql_validation_service.validate_sql_query(sql_query=self.sql_query,schema_component=schema_components)

            # 4. Execute SQL Query with retry logic using DatabaseExecuteService

            result_df = self.db_executor.execute_sql_query(sql_query=self.sql_query)

            self.logger.info(f"User Query process and result : {result_df}")

            # 5. Format LLM Response
            result = {
                "status": "success",
                "sql_query" : self.sql_query,
                "results": result_df.to_dict(orient='records'),
                "row_count": len(result_df),
            }

            return result

        except Exception as e:
            self.logger.error(f"SQL Query processing failed: {e}")
            result = {
                "status": "Failed",
                "sql_query" : self.sql_query,
                "results": [],
                "row_count": 0,
                "message": "Error while procesing user query"
            }
            return result

    

    def _process_db_schema(self,db_schema_path: str = settings.db_schema_path):

        self.logger.info("processing db schema")

        with open(db_schema_path, 'r') as file:
         schema = json.load(file)

        return schema


if __name__=="__main__":
        sql_processing_service = SQLProcessingService(user_query="Employee count in Finsolve Technologies")
        result = sql_processing_service.process_user_query()
        print(f"User Query: {sql_processing_service.user_query}")
        print(f"SQL query: {sql_processing_service.sql_query}")
        print(f"Result: {result}")





