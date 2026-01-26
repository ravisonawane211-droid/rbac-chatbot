from typing import Dict, Any, List
import json

class SQLGenerationPrompts:

    @staticmethod
    def get_sql_generation_prompt(
        user_query: str,
        schema: Dict[str, Any], 
        entities: Dict[str, Any], 
        joins: List
    ):
            prompt_parts = ["""
                You are an expert PostgreSQL developer specializing in queries.

                Your task is to generate a syntactically correct, optimized, and safe PostgreSQL SQL query based on the inputs provided.
                """]

            prompt_parts.append("#Inputs")

            prompt_parts.append(f"\nUser Query in natural language text:\n{user_query}")
            prompt_parts.append(f"\nDatabase Schema in JSON format:\n{json.dumps(schema,indent=2)}")

            # 👉 Conditionally add entities
            if entities and len(entities)>0:
                entity_block = "\nKnown Entities extracted from user_query are below. These will be used in SQL WHERE clause :\n"
                for k, v in entities.items():
                    entity_block += f"- {k} = {v}\n"
                prompt_parts.append(entity_block.strip())

            # 👉 Conditionally add joins
            if joins and len(joins)>0:
                prompt_parts.append(f"\nAllowed Joins:\n{joins}")

            rules = """
        RULES:
        1. Use ONLY the tables and columns present in the schema.
        2. Use PostgreSQL compatible syntax only.
        3. Never hallucinate tables or columns.
        4. Always qualify columns with table aliases when multiple tables are used.
        5. Prefer INNER JOIN unless the user asks for missing data.
        6. Apply entity filters when column names match.
        7. If aggregation is required, use GROUP BY correctly.
        8. If ordering is implied, use ORDER BY.
        9. Limit results to 100 rows unless user specifies otherwise.
        10. Use safe casting for dates and numbers.
        11. Do not modify data (no INSERT, UPDATE, DELETE, DROP).
        12. Return only the SQL query, no explanation or markdown.
        """
            prompt_parts.append(rules.strip())

            prompt_parts.append(""" \n
        OUTPUT FORMAT:\n
         Return strictly valid PostgreSQL query in JSON:\n
         { "sql": "<PostgreSQL SELECT query only>" }
       
        """.strip())

            return "\n".join(prompt_parts)
    

    @staticmethod
    def get_error_retry_sql_generation_prompt(
        user_query: str,
        schema: Dict[str, Any], 
        entities: Dict[str, Any], 
        joins: List,
        error_info: str
    ):
            prompt_parts = [f"""
                You are an expert PostgreSQL developer specializing in queries.

                Your task is to generate a corrected SQL query that addresses the specific eror from the previous attempt.
                            
                #Previous Error Information:
                 {error_info}            
                """]

            prompt_parts.append("#Inputs")

            prompt_parts.append(f"\nUser Query in natural language text:\n{user_query}")
            prompt_parts.append(f"\nDatabase Schema in JSON format:\n{json.dumps(schema,indent=2)}")

            # 👉 Conditionally add entities
            if entities and len(entities)>0:
                entity_block = "\nKnown Entities extracted from user_query are below. These will be used in SQL WHERE clause :\n"
                for k, v in entities.items():
                    entity_block += f"- {k} = {v}\n"
                prompt_parts.append(entity_block.strip())

            # 👉 Conditionally add joins
            if joins and len(joins)>0:
                prompt_parts.append(f"\nAllowed Joins:\n{joins}")

            rules = """
        RULES:
        1. Use ONLY the tables and columns present in the schema.
        2. Use PostgreSQL compatible syntax only.
        3. Never hallucinate tables or columns.
        4. Always qualify columns with table aliases when multiple tables are used.
        5. Prefer INNER JOIN unless the user asks for missing data.
        6. Apply entity filters when column names match.
        7. If aggregation is required, use GROUP BY correctly.
        8. If ordering is implied, use ORDER BY.
        9. Limit results to 100 rows unless user specifies otherwise.
        10. Use safe casting for dates and numbers.
        11. Do not modify data (no INSERT, UPDATE, DELETE, DROP).
        12. Return only the SQL query, no explanation or markdown.
        """
            prompt_parts.append(rules.strip())

            prompt_parts.append(""" \n
        OUTPUT FORMAT:\n
         Return strictly valid PostgreSQL query in JSON:\n
         { "sql": "<PostgreSQL SELECT query only>" }
       
        """.strip())

            return "\n".join(prompt_parts)
        