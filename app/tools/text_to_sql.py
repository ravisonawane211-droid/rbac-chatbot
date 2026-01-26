from langchain_core.tools import tool
from app.services.sql_processing_service import SQLProcessingService
from typing import List,Dict, Any
from app.utils.logger import get_logger


logger = get_logger(__name__)

@tool("text_to_sql",description="This tool takes question and gnerates to sql query and executes it and return result")
def text_to_sql(question: str, roles: List[str]) -> Dict[str, Any]:
    """
    Executes a natural language query against Postgres using the internal SQL service.
    The service loads schema from JSON, generates SQL, validates it, and runs it safely.
    Input: natural language question.
    Output: dict with sql_query, results, row_count
    """
    logger.info(f"inside text_to_sql tool with user_query: {question}")

    sql_processing_service = SQLProcessingService(user_query=question , roles=roles)

    sql_result = sql_processing_service.process_user_query()

    logger.info(f"received response from SQLProcessingService: {sql_result}")

    return sql_result

    # If HTTP microservice:
    # resp = requests.post("http://localhost:8001/run-sql", json={"question": question})
    # return resp.json()
