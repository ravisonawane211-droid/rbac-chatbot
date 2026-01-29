from app.utils.logger import get_logger
from typing import Dict, Any
import re
import sqlglot

class SQLValidationSerice:

    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("SQLValidationSerice initialized")
        

    def validate_sql_query(self,sql_query: str, schema_component: Dict[str, Any] = None, allowed_tables:list=[]):
        
        try:
            self.logger.info("Starting SQL query validatons: ")

            self._validate_against_role(sql_query=sql_query, allowed_tables=allowed_tables)
            self._validate_basic_syntax(sql_query=sql_query)
            self._validate_against_schema(sql_query=sql_query,schema_component=schema_component)

            self.logger.info("SQL Query validation successfull.")
        except Exception as e:
            self.logger.error(f"Error while validating sql query {e}")
            raise e

    def _validate_against_role(self,sql_query:str, allowed_tables:list=[]):

        self.logger.info(f"Validating role to access tables in query")
        
        if self._validate_tables(sql_query=sql_query, allowed_tables=allowed_tables,alias_map = {}):
            raise Exception("Your role does not allow access to the data needed for this request.")
        
        self.logger.info("Validating role to access tables in query completed")


    def _validate_basic_syntax(self, sql_query: str):

        self.logger.info("Validating basic syntax of quey: ")

        if self._validate_structure(sql_query=sql_query):
            raise Exception("SQL query validation failed due to syntax error in query.Please verify generated query.")
        
        if self._validate_security(sql_query=sql_query):
            raise Exception("SQL query validation failed due to unsafe database operation.Please verify generated query.")
        

    def _validate_against_schema(self, sql_query: str, schema_component: Dict[str, Any] = None):
        self.logger.info("validating sql query agains schema")

        tables = schema_component.get("schema",[])

        valid_tables = [table.get("table_name","") for table in tables]

        schema_map = {
            table.get("table_name"): table.get("columns", [])
            for table in tables
        }       

        alias_map = {}

        if self._validate_tables(sql_query=sql_query, allowed_tables=valid_tables,alias_map = alias_map):
            raise Exception("SQL query validation failed due to invalid table in query.Please verify generated query.")
        
        if self._validate_columns(sql_query=sql_query, schema_map=schema_map,alias_map = alias_map):
            raise Exception("SQL query validation failed due to invalid column in query.Please verify generated query.")


    def _validate_structure(self, sql_query: str):
        self.logger.info("validating sql query structure")

        s = sql_query.strip().lower()
        if not s.startswith(("select", "with")):
            return True

        if s.count(";") > 1:
            return True
        
        return False
    
    def _validate_security(self, sql_query: str):
        self.logger.info("validating database safe operation in sql query")

        blocked = r"\b(insert|update|delete|drop|alter|truncate|merge|create|grant|revoke)\b"
        if re.search(blocked, sql_query, re.IGNORECASE):
            return True
        else:
            return False
        
    
    def _validate_tables(self, sql_query: str, allowed_tables:list, alias_map : dict):
        self.logger.info("validating valid tables in sql query")
        parsed = sqlglot.parse_one(sql_query)

        for table in parsed.find_all(sqlglot.exp.Table):
            alias = table.alias_or_name
            alias_map[alias] = table.this
            if table.name not in allowed_tables:
                return True
        return False
    
    def _validate_columns(self, sql_query, schema_map:Dict[str, Any], alias_map : dict):
        self.logger.info("validating valid coulmns in sql query")

        parsed = sqlglot.parse_one(sql_query)
        for col in parsed.find_all(sqlglot.exp.Column):
            alias = col.table
            name = col.name

            if alias:  
                table_real = alias_map.get(alias).name
                if not table_real:
                    raise ValueError(f"Unknown table alias: {alias}")
            else:
                table_real = None
            
            column_list = [col.get("name","") for col in schema_map.get(table_real, []) if table_real]

            if name not in column_list:
                raise ValueError(f"Invalid column {table}.{name}")


        