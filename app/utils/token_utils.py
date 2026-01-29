import jwt
import time
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_access_token(user_id:str,password:str,roles:str, secret_key: str, conversation_id:str , algorithm: str="HS256",expire_minutes:int=15) -> str:
    """Create a JWT access token."""
    logger.info(f"Creating access token for user_id: {user_id}")
    data = {"user_id": user_id, "password": password,"roles":roles,"conversation_id":conversation_id, 
            "expires_in": time.time() + expire_minutes * 60}
    return jwt.encode(data, secret_key, algorithm=algorithm)

def decode_access_token(token: str, secret_key: str, algorithms: list) -> dict:
    """Decode a JWT access token."""
    logger.info("Decoding access token")
    decoded_token = jwt.decode(token, secret_key, algorithms=algorithms)
    return decoded_token if decoded_token["expires_in"] >= time.time() else None

