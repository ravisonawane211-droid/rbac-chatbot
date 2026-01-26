from typing import Dict,Any
from app.utils.logger import get_logger
from app.services.llm_service import LLMService
from app.config.config import get_settings
from app.prompts.sql_generation import SQLGenerationPrompts
import json

settings = get_settings()

class SQLGenerationService:

    def __init__(self,llm_provider: str = None, llm_model: str = None) -> str :
        self.logger = get_logger(__name__)

        self.llm_service = LLMService(llm_provider=llm_provider, llm_model=llm_model)
        self.logger.info(f"SQLGenerationService initialized with {llm_provider} {llm_model}")


    def generate_sql_query(self, user_query: str, entities: Dict[str,Any], schema_components: Dict[str, Any]) -> str:
        
        try:
            self.logger.info(f"Generating SQL for query: {user_query}")
            
            prompt = self._build_sql_prompt(user_query=user_query, entities= entities, schema_components=schema_components)

            self.logger.info(f"Final prompt generated : {prompt}")

            message_content = self.llm_service.generate_response(prompt=prompt,
                                            temperature=settings.llm_temperature)
            
            sql_query = self._extract_sql_from_response(response=message_content.content)

            if not sql_query:
                raise Exception("Failed to extract valid SQL query from LLM response")
            
            return sql_query
        
        except Exception as e:
            self.logger.error(f"SQL query generation failed {e}")
            raise e
        
    
    def regenerate_sql_query_with_error(self, user_query: str, entities: Dict[str,Any], schema_components: Dict[str, Any],error_info: str) -> str:
        
        try:
            self.logger.info(f"Generating SQL for query: {user_query}")
            
            prompt = self._build_error_retry_sql_prompt(user_query=user_query, entities= entities, 
                                                        schema_components=schema_components,
                                                        error_info=error_info)

            self.logger.info(f"Final prompt generated : {prompt}")

            message_content = self.llm_service.generate_response(prompt=prompt,
                                            temperature=settings.llm_temperature)
            
            sql_query = self._extract_sql_from_response(response=message_content.content)

            if not sql_query:
                raise Exception("Failed to extract valid SQL query from LLM response")
            
            return sql_query
        
        except Exception as e:
            self.logger.error(f"SQL query re-generation failed {e}")
            raise e
        

    def _build_sql_prompt(self,user_query: str, entities: Dict[str,Any], schema_components: Dict[str, Any]):

        self.logger.info(f"Builing sql prompt for user_query: {user_query}")

        tables = schema_components.get("schema", [])

        joins = [table.get("joins",[]) for table in tables]

        schema = self._remove_joins(schema_components)

        prompt = SQLGenerationPrompts.get_sql_generation_prompt(
            user_query=user_query,
            schema=schema,
            entities=entities,
            joins=joins)
        
        self.logger.info(f"SQL generation prompt generated: {prompt}")

        return prompt

    def _remove_joins(self, schema_components):
        schema_copy = schema_components.copy()

        for table in schema_copy.get("schema", []):
            table.pop("joins", None)
        return schema_copy
    

    def _build_error_retry_sql_prompt(self,user_query: str, entities: Dict[str,Any], 
                                      schema_components: Dict[str, Any],
                                      error_info: SyntaxError) -> str:

        self.logger.info(f"Builing sql prompt for user_query: {user_query}")

        schema = schema_components.get("schema", [])

        joins = schema_components.get("joins", [])

        prompt = SQLGenerationPrompts.get_error_retry_sql_generation_prompt(
            user_query=user_query,
            schema=schema,
            entities=entities,
            joins=joins,
            error_info=error_info
            )
        
        self.logger.info(f"SQL generation prompt generated: {prompt}")

        return prompt
    
    def _extract_sql_from_response(self, response: str) -> str:
        self.logger.info(f"extracting sql_query form llm response: {response}")
        response = response.replace("```","").replace("json","").replace("```","")
        data = json.loads(response)

        if "sql" not in data:
            raise ValueError("Missing 'sql' field")

        if not isinstance(data["sql"], str):
            raise ValueError("SQL must be string")

        return data["sql"].strip()



        
        


    
