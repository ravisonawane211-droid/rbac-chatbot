from fastapi import APIRouter, HTTPException,Depends
from app.services.auth_service import AuthService
from app.schemas.user import User
from app.schemas.login_response import LoginResponse
from app.schemas.login_request import LoginRequest
from app.schemas.create_user_request import CreateUserRequest
from app.schemas.create_user_response import CreateUserResponse
from app.auth.jwt_bearer import JWTBearer
from app.services.db_service import DatabaseService
from app.utils.token_utils import create_access_token
from app.config.config import get_settings
from app.utils.logger import get_logger
import uuid
import pandas as pd


router = APIRouter(prefix="/users", tags=["Users"])

settings = get_settings()
logger = get_logger(__name__)
auth_scheme = JWTBearer()

@router.post(path="",
             summary="Create a new user",
             description="Create a new user with the provided details.")
def create_user(create_user_request:CreateUserRequest,user_info: dict =Depends(auth_scheme)):
    """
    Create a new user.
    Args:
        create_user_request (CreateUserRequest): The request containing user details.
    Returns:
        CreateUserResponse: The response confirming user creation.
    """
    logger.info(f"creating user with user_name {create_user_request.user.user_id} ,requested by {user_info["user_id"]}")

    if create_user_request.user == None:
        raise HTTPException(status_code=400, detail="User details are required")
    
    if not create_user_request.user.user_id or not create_user_request.user.password or not create_user_request.user.user_role:
        raise HTTPException(status_code=400, detail="User name, password and role are required")
    
    db_service = DatabaseService()
    user_df = pd.DataFrame([{"user_id": create_user_request.user.user_id,"password": create_user_request.user.password,
                   "user_role": create_user_request.user.user_role[0]}])

    db_service.save_dataframe_to_table(df=user_df,table_name="users")

    logger.info(f"User {create_user_request.user.user_id} created successfully")

    create_user_response = CreateUserResponse(
        message=f"User {create_user_request.user.user_id} created successfully",
        status="success",
        user_name=create_user_request.user.user_id,
        user_role=create_user_request.user.user_role
    )
    return create_user_response


@router.post("/login")
def login(login_request:LoginRequest):
    """
    User login endpoint.
    Args:
        login_request (LoginRequest): The login request containing username and password.
    Returns:
        LoginResponse: The response containing user details and access token.

    """
    logger.info("Attempting login for user: {login_request.user_name}")

    if login_request.user_name is None or login_request.password is None:
        raise HTTPException(status_code=400, detail="Username and password are required")

    authenticated_user:User = _authenticate(login_request.user_name,login_request.password)
    
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        access_token=create_access_token(authenticated_user.user_id,authenticated_user.password,authenticated_user.user_role,
                                             settings.secret_key,settings.algorithm)
        authenticated_user.password = None

        conversation_id = str(uuid.uuid4())
        
        login_response = LoginResponse(
            message=f"Welcome {authenticated_user.user_id}!",
            status="success",
            user=authenticated_user,
            access_token = access_token,
            conversation_id=conversation_id
        )
        logger.info(f"User {login_request.user_name} logged in successfully")
    return login_response

def _authenticate(user_name:str, password: str) -> User:

    auth_service = AuthService()

    user = auth_service.authenticate(user_name, password)
    return user




