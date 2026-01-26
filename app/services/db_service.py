
from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator
import sys
from pathlib import Path
from typing import Optional

# When running app/main.py directly (e.g. `python app/main.py`), Python
# doesn't treat `app` as an installed package, so `from app import ...`
# fails. Add project root to sys.path as a fallback so package imports work
# when invoked directly (this keeps behavior consistent for debugging).
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.config.config import get_settings
from app.utils.logger import get_logger


settings = get_settings()
logger = get_logger(__name__)

def get_sqlite_db(db_path: str, enable_foreign_keys: bool = True) -> sqlite3.Connection:
    """Get a SQLite database connection."""

    logger.info(f"Connecting to database at {db_path}")
    
    path = Path(db_path) if db_path else settings.database_url
    conn = sqlite3.connect(str(path), detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    if enable_foreign_keys:
        conn.execute("PRAGMA foreign_keys = ON;")
    logger.info(f"Connected to database at {path}")
    return conn

class DatabaseService:
    def __init__(self, db_path: Optional[str] = settings.database_url, enable_foreign_keys: bool = True):
        
        self.conn = get_sqlite_db(db_path, enable_foreign_keys)

        logger.info("DatabaseService initialized.")

    
    @contextmanager
    def get_db(self) -> Iterator[sqlite3.Connection]:
        """Context manager for a database connection that always closes on exit."""
        conn = self.conn 
        try:
            yield conn
        finally:
            logger.info("Closing database connection.")
            conn.close()

    
    def save_dataframe_to_table(self, df, table_name: str, if_exists: str = 'append'):
        """Saves a pandas DataFrame to a specified table in the database."""
        logger.info(f"Saving DataFrame to table '{table_name}' with if_exists='{if_exists}'")
        df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)
        logger.info(f"DataFrame saved to table '{table_name}' with if_exists='{if_exists}'")

    
    def get_schema(self) -> str:
        """Return the DB schema as a single string (skips internal sqlite tables)."""
        logger.info("Retrieving database schema.")
        
        query = "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        
        with self.get_db() as conn:
            rows = conn.execute(query).fetchall()
        parts = []
        for row in rows:
            name = row["name"]
            create_sql = row["sql"] or ""
            parts.append(f"-- Table: {name}\n{create_sql}")
        schema_str = "\n\n".join(parts)
        logger.info(f"Retrieved database schema {schema_str} for {len(rows)} tables.")
        return schema_str

    