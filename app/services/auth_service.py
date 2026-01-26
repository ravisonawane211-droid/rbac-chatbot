from app.services.db_service import DatabaseService
from app.utils.logger import get_logger
from app.schemas.user import User
from typing import Optional
from functools import lru_cache

logger = get_logger(__name__)

@lru_cache
def get_user(username:str,db_service:DatabaseService):
    logger.info(f"Authenticating user: {username}")
        
    user: Optional[User] = None

    with db_service.get_db() as conn:
        cursor = conn.execute(
                "SELECT employee_id,user_id,password,user_role FROM users WHERE user_id = ?", (username,)
        )
        row = cursor.fetchone()
        if row:
            user = User(
                    user_id=row["user_id"],
                    email=None,
                    user_role=str(row["user_role"]).split(","),
                    password=row["password"]
                )
    return user


class AuthService:
    
    def __init__(self):
        self.db_service = DatabaseService(db_path="./resources/data/db/rbac_chatbot.db")


    def authenticate(self, username: str, password: str) -> User | None:
        """Authenticates a user against the database."""
        logger.info(f"Authenticating user: {username}")
        
        user: Optional[User] = get_user(username,self.db_service)
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