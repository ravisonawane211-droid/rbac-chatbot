from app.utils.logger import get_logger
from typing import Dict, Any
import re
import sqlglot

class SQLValidationSerice:

    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("SQLValidationSerice initialized")
        

    def validate_sql_query(self,sql_query: str, schema_component: Dict[str, Any] = None, allowed_tables:list=[], user_info: dict = {}):
        
        try:
            self.logger.info("Starting SQL query validatons: ")

            self._validate_against_role(sql_query=sql_query, allowed_tables=allowed_tables)
            self._validate_basic_syntax(sql_query=sql_query)
            self._validate_against_schema(sql_query=sql_query,schema_component=schema_component)
            #self._validate_employee_leave_access(sql_query=sql_query, user_info=user_info)

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
    
    def _validate_columns(self, sql_query, schema_map:Dict[str, Any], alias_map : dict):
        self.logger.info("validating valid coulmns in sql query")

        parsed = sqlglot.parse_one(sql_query)
        cte_columns = {}
        for cte in parsed.find_all(sqlglot.exp.CTE):
            cte_name = cte.alias_or_name.lower()
            column_names = []
            for select in cte.this.selects:
                selected_name = select.alias_or_name or getattr(getattr(select, "this", None), "name", None) or getattr(select, "name", None)
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

    def _validate_employee_leave_access(self, sql_query: str, user_info: dict = {}):
        """
        Validate that queries accessing employee_leave table are filtered by the logged-in user's employee_id.
        This ensures users can only access their own leave balance.
        """
        self.logger.info("Validating employee_leave table access")
        
        try:
            parsed = sqlglot.parse_one(sql_query)
            
            # Check if the query accesses employee_leave table
            tables = [table.name for table in parsed.find_all(sqlglot.exp.Table)]
            
            if "employee_leave" not in tables:
                self.logger.info("Query does not access employee_leave table, skipping employee_leave validation")
                return
            
            # Get the logged-in user's employee_id
            user_employee_id = user_info.get("employee_id")
            if not user_employee_id:
                raise Exception("User information is missing employee_id. Cannot validate leave balance access.")
            
            self.logger.info(f"Employee leave access validation: checking if query filters by employee_id {user_employee_id}")
            
            # Extract all WHERE conditions
            where_clauses = parsed.find_all(sqlglot.exp.Where)
            
            if not where_clauses:
                raise Exception(f"Access Denied: Employee leave balance queries must filter by employee_id. Cannot access data without user identification.")
            
            # Check if any WHERE condition filters by the user's employee_id
            found_valid_filter = False
            
            for where_clause in where_clauses:
                # Look for conditions comparing employee_id with the user's employee_id
                conditions = self._extract_where_conditions(where_clause)
                
                for condition in conditions:
                    # Check if the condition involves employee_id and the user's employee_id value
                    if self._has_employee_id_filter(condition, user_employee_id):
                        found_valid_filter = True
                        break
                
                if found_valid_filter:
                    break
            
            if not found_valid_filter:
                raise Exception(
                    f"Access Denied: You can only query leave balance for employee_id '{user_employee_id}'. "
                    f"Your query attempted to access employee_leave table without filtering by your employee_id."
                )
            
            self.logger.info(f"Employee leave access validation passed for employee_id {user_employee_id}")
        
        except sqlglot.ParseError as e:
            self.logger.error(f"Could not parse SQL for employee_leave validation: {e}")
            # If we can't parse, allow it to pass (other validators will catch issues)
        except Exception as e:
            self.logger.error(f"Employee leave access validation failed: {e}")
            raise

    def _extract_where_conditions(self, where_clause):
        """
        Extract individual conditions from a WHERE clause.
        Handles AND, OR, and other logical operators.
        """
        conditions = []
        
        # Try to find all comparison expressions
        for comp in where_clause.find_all(sqlglot.exp.EQ):
            conditions.append(comp)
        
        # Also include other comparison operators
        for comp_type in [sqlglot.exp.NEQ, sqlglot.exp.LT, sqlglot.exp.LTE, 
                          sqlglot.exp.GT, sqlglot.exp.GTE]:
            for comp in where_clause.find_all(comp_type):
                conditions.append(comp)
        
        return conditions if conditions else [where_clause]

    def _has_employee_id_filter(self, condition, user_employee_id: str) -> bool:
        """
        Check if a condition filters by the user's employee_id.
        Returns True if the condition involves employee_id and matches the user's employee_id.
        """
        try:
            condition_str = str(condition).lower()
            
            # Check if employee_id or employee.employee_id is mentioned
            if "employee_id" not in condition_str:
                return False
            
            # Check if the user's employee_id value appears in the condition
            # This catches conditions like: WHERE employee_id = 'FINEMP1000'
            if user_employee_id.lower() in condition_str or user_employee_id.upper() in condition_str:
                return True
            
            # For values in params or parameterized queries, we can check structure
            # Look for patterns like: employee_id = <value>
            left = condition.left if hasattr(condition, 'left') else None
            right = condition.right if hasattr(condition, 'right') else None
            
            if left and right:
                left_str = str(left).lower()
                right_str = str(right).lower()
                
                # Check if left side is employee_id and right side contains user's employee_id
                if "employee_id" in left_str:
                    if user_employee_id.lower() in right_str or user_employee_id.upper() in right_str:
                        return True
                
                # Check reverse
                if "employee_id" in right_str:
                    if user_employee_id.lower() in left_str or user_employee_id.upper() in left_str:
                        return True
            
            return False
        except Exception as e:
            self.logger.warning(f"Error checking employee_id filter: {e}")
            return False