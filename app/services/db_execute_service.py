from sqlalchemy import create_engine
from app.config.config import get_settings
from app.utils.logger import get_logger
import threading
import pandas as pd
import time
from typing import Optional

settings = get_settings()

class DatabaseExecuteService:

    def __init__(self,timeout_seconds: int = 120):
        self.timeout_seconds = timeout_seconds
        self.logger = get_logger(__name__)
        self.logger.info(f"DatabaseExecutorService initialised with timeout_seconds {self.timeout_seconds}")


    def _execute_query_with_timeout(self , sql_query : str, db_config : Optional[str]):

        result_df = [None]
        exception = [None]

        start_time = time.time()

        try:
            
            engine = create_engine(url=db_config)

            def worker():
                try:
                    with engine.connect() as connection:
                        result_df[0] = pd.read_sql(sql=sql_query,con=connection)
                except Exception as e:
                    self.logger.error(f"error while executing query: {e}")
                    exception[0] = e

            query_thread = threading.Thread(target=worker)
            query_thread.daemon = True
            query_thread.start()
            while query_thread.is_alive():
                elapsed_time = time.time() - start_time

                if elapsed_time > self.timeout_seconds:
                    self.logger.error(f"SQL query execution timout after {elapsed_time:.2f} seconds | Limit: {self.timeout_seconds}s")
                    raise Exception(f"SQL query execution timout after {elapsed_time:.2f} seconds | Limit: {self.timeout_seconds}s"
                                    "The query is too complex or incorrect.Please review and optimize SQL query.")
                
            time.sleep(0.1)
            execution_time = time.time() - start_time
            self.logger.info(f"SQL query execution completed in {execution_time:.2f} seconds")

            if exception[0] is not None:
                raise exception[0]
            
            # get the result and standardize column names
            result_df:pd.DataFrame = result_df[0]
            if result_df is not None and not result_df.empty:
                result_df.columns = map(str.lower,result_df.columns)
                self.logger.info(f"SQL  query executed successfully | Retrived {len(result_df)} rows")

            return result_df
        except Exception as e:
            self.logger.error(f"error while executing query : {e}")

    
    def execute_sql_query(self,sql_query: str, db_config:Optional[str] = None) -> Optional[pd.DataFrame] :
        
        try:
            if db_config is None:
                db_config = settings.database_url

            self.logger.info(f"Executing SQL query : {sql_query[:200]} ...")

            result_df = self._execute_query_with_timeout(sql_query=sql_query,db_config=db_config)

            if result_df is not None:
                self.logger.info(f"SQL  query executed successfully | Retrived {len(result_df)} rows")
            else:
                self.logger.warning("SQL query execution returned no rows")

            return result_df
        except Exception as e:
            self.logger.error(f"error occurred while executing query : {e}")
            return None



        

                

