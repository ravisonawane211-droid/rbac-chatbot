from app.services.db_execute_service import DatabaseExecuteService
from app.utils.logger import get_logger
from app.schemas.user import User
from typing import Optional
from functools import lru_cache
from app.config.config import get_settings

logger = get_logger(__name__)
settings = get_settings()

@lru_cache
def get_user(username:str,db_service:DatabaseExecuteService):
    logger.info(f"Authenticating user: {username}")
        
    user: Optional[User] = None

    user_df = db_service.execute_sql_query(sql_query=f"SELECT employee_id,user_id,password,user_role FROM users WHERE user_id = '{username}'")

    if not user_df.empty:
        row = user_df.iloc[0]
        user = User(
                    user_id=row["user_id"],
                    email=row["user_id"],
                    user_role=str(row["user_role"]).split(","),
                    password=row["password"]
                )
        
    return user


class AuthService:
    
    def __init__(self):
        self.db_executor_service = DatabaseExecuteService(db_config=settings.database_url)


    def authenticate(self, username: str, password: str) -> User | None:
        """Authenticates a user against the database."""
        logger.info(f"Authenticating user: {username}")
        
        user: Optional[User] = get_user(username,self.db_executor_service)
        if user:
            is_authenticated = self.verify_password(password, user.password)
            logger.info(f"User '{username}' authentication result: {is_authenticated}")
            return user if is_authenticated else None
        else:
            logger.warning(f"User '{username}' not found in database.")
            return None
            
    def verify_password(self, plain_password: str, stored_password: str) -> bool:
        """Verifies a plain entered password against a stored password."""
        # Placeholder for actual password verification logic
        return plain_password == stored_password  # Simplified for demonstration