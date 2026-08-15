import jwt
import time
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _create_token(user_id:str, employee_id:str, password:str, roles:str, secret_key: str,
                 conversation_id:str, algorithm: str, expire_minutes:int, token_type:str) -> str:
    logger.info(f"Creating {token_type} token for user_id: {user_id}")
    data = {
        "user_id": user_id,
        "employee_id": employee_id,
        "password": password,
        "roles": roles,
        "conversation_id": conversation_id,
        "token_type": token_type,
        "expires_in": time.time() + expire_minutes * 60,
    }
    return jwt.encode(data, secret_key, algorithm=algorithm)


def create_access_token(user_id:str,employee_id:str, password:str,roles:str, secret_key: str,
                       conversation_id:str , algorithm: str="HS256",expire_minutes:int=15) -> str:
    """Create a JWT access token."""
    return _create_token(
        user_id=user_id,
        employee_id=employee_id,
        password=password,
        roles=roles,
        secret_key=secret_key,
        conversation_id=conversation_id,
        algorithm=algorithm,
        expire_minutes=expire_minutes,
        token_type="access",
    )


def create_refresh_token(user_id:str,employee_id:str, password:str,roles:str, secret_key: str,
                        conversation_id:str , algorithm: str="HS256",expire_minutes:int=10080) -> str:
    """Create a JWT refresh token with a longer lifetime."""
    return _create_token(
        user_id=user_id,
        employee_id=employee_id,
        password=password,
        roles=roles,
        secret_key=secret_key,
        conversation_id=conversation_id,
        algorithm=algorithm,
        expire_minutes=expire_minutes,
        token_type="refresh",
    )


def decode_token(token: str, secret_key: str, algorithms: list | str, expected_type: str | None = None) -> dict | None:
    """Decode a JWT token and validate expiry and expected type."""
    try:
        logger.info("Decoding token")
        decoded_token = jwt.decode(token, secret_key, algorithms=algorithms)
        if expected_type and decoded_token.get("token_type") != expected_type:
            logger.warning("Token type mismatch: expected %s but got %s", expected_type, decoded_token.get("token_type"))
            return None
        if decoded_token.get("expires_in") is None or decoded_token["expires_in"] < time.time():
            logger.warning("Token expired")
            return None
        return decoded_token
    except Exception as exc:
        logger.warning("Token decode failed: %s", exc)
        return None


def decode_access_token(token: str, secret_key: str, algorithms: list | str) -> dict | None:
    """Decode a JWT access token."""
    return decode_token(token, secret_key, algorithms, expected_type="access")


def decode_refresh_token(token: str, secret_key: str, algorithms: list | str) -> dict | None:
    """Decode a JWT refresh token."""
    return decode_token(token, secret_key, algorithms, expected_type="refresh")

