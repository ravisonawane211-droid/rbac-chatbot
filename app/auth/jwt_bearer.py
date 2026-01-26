from fastapi import Request, HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.token_utils import decode_access_token
from app.services.auth_service import AuthService
from app.utils.logger import get_logger
from app.config.config import get_settings

settings = get_settings()
logger = get_logger(__name__)

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        logger.info("JWTBearer initialized")

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        auth_service = AuthService()
        if credentials:
            if not credentials.scheme == "Bearer":
                logger.error("Invalid authentication scheme")
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            decoded_payload = self.verify_jwt(credentials.credentials,auth_service)
            if not decoded_payload:    
                logger.error("Invalid token or expired token")
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            logger.info("JWT token successfully verified")
            return decoded_payload
        else:
            logger.error("Invalid authorization code")
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str, auth_service: AuthService) -> bool:
        try:
            logger.info("Verifying JWT token")
            payload = decode_access_token(token=jwtoken,secret_key=settings.secret_key,algorithms=settings.algorithm)
            user_id = payload['user_id']
            password = payload['password']
            user = auth_service.authenticate(user_id, password)
      
            if not user or user.password != password:
                logger.error(f"Token verification failed: user not found or password mismatch for user_id {user_id}")
            
            if payload and user.password == password:
                logger.info(f"Token successfully verified for user_id {user_id}")
                return payload
        except Exception as e:
            logger.error(f"Token verification failed due to error : {e}")

        return None