import uuid

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth.jwt_bearer import JWTBearer
from app.config.config import get_settings
from app.schemas.create_user_request import CreateUserRequest
from app.schemas.create_user_response import CreateUserResponse
from app.schemas.login_request import LoginRequest
from app.schemas.login_response import LoginResponse
from app.schemas.user import User
from app.services.auth_service import AuthService
from app.services.db_execute_service import DatabaseExecuteService
from app.utils.logger import get_logger
from app.utils.token_utils import create_access_token, create_refresh_token, decode_refresh_token

router = APIRouter(prefix="/users", tags=["Users"])
settings = get_settings()
logger = get_logger(__name__)
auth_scheme = JWTBearer()


@router.post(
    path="",
    summary="Create a new user",
    description="Create a new user with the provided details.",
)
def create_user(create_user_request: CreateUserRequest, user_info: dict = Depends(auth_scheme)):
    """Create a new user with the provided details."""
    logger.info(
        f"Creating user with user_name {create_user_request.user.user_id}, requested by {user_info['user_id']}"
    )

    if create_user_request.user is None:
        raise HTTPException(status_code=400, detail="User details are required")

    if (
        not create_user_request.user.user_id
        or not create_user_request.user.password
        or not create_user_request.user.user_role
    ):
        raise HTTPException(status_code=400, detail="User name, password and role are required")

    database_execute_service = DatabaseExecuteService(db_config=settings.database_url)
    user_df = pd.DataFrame(
        [{
            "user_id": create_user_request.user.user_id,
            "password": create_user_request.user.password,
            "user_role": create_user_request.user.user_role[0],
        }]
    )
    database_execute_service.save_dataframe_to_table(df=user_df, table_name="users")

    logger.info(f"User {create_user_request.user.user_id} created successfully")

    return CreateUserResponse(
        message=f"User {create_user_request.user.user_id} created successfully",
        status="success",
        user_name=create_user_request.user.user_id,
        user_role=create_user_request.user.user_role,
    )


@router.post("/login")
async def login(request: Request):
    """User login endpoint supporting JSON and form-encoded payloads."""
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type.lower():
            payload = await request.json()
            login_request = LoginRequest.model_validate(payload)
            user_name = login_request.user_name
            password = login_request.password
        else:
            form_data = await request.form()
            user_name = form_data.get("user_name") or form_data.get("username")
            password = form_data.get("password")
    except Exception:
        user_name = None
        password = None

    if not user_name or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    logger.info(f"Attempting login for user: {user_name}")

    authenticated_user: User = _authenticate(user_name, password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    conversation_id = str(uuid.uuid4())
    access_token = create_access_token(
        user_id=authenticated_user.user_id,
        employee_id=authenticated_user.employee_id,
        password=authenticated_user.password,
        roles=authenticated_user.user_role,
        secret_key=settings.secret_key,
        conversation_id=conversation_id,
        algorithm=settings.algorithm,
    )
    refresh_token = create_refresh_token(
        user_id=authenticated_user.user_id,
        employee_id=authenticated_user.employee_id,
        password=authenticated_user.password,
        roles=authenticated_user.user_role,
        secret_key=settings.secret_key,
        conversation_id=conversation_id,
        algorithm=settings.algorithm,
    )
    authenticated_user.password = None

    logger.info(f"User {user_name} logged in successfully")
    return LoginResponse(
        message=f"Welcome {authenticated_user.user_id}!",
        status="success",
        user=authenticated_user,
        access_token=access_token,
        refresh_token=refresh_token,
        conversation_id=conversation_id,
    )


@router.post("/refresh")
async def refresh(request: Request):
    """Refresh an expired access token using a valid refresh token."""
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    refresh_token = payload.get("refresh_token") or request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is required.")

    decoded = decode_refresh_token(refresh_token, settings.secret_key, settings.algorithm)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token.")

    auth_service = AuthService()
    user = auth_service.authenticate(decoded["user_id"], decoded["password"])
    if not user:
        raise HTTPException(status_code=401, detail="User session could not be validated.")

    conversation_id = decoded.get("conversation_id") or str(uuid.uuid4())
    new_access_token = create_access_token(
        user_id=user.user_id,
        employee_id=user.employee_id,
        password=user.password,
        roles=user.user_role,
        secret_key=settings.secret_key,
        conversation_id=conversation_id,
        algorithm=settings.algorithm,
    )
    new_refresh_token = create_refresh_token(
        user_id=user.user_id,
        employee_id=user.employee_id,
        password=user.password,
        roles=user.user_role,
        secret_key=settings.secret_key,
        conversation_id=conversation_id,
        algorithm=settings.algorithm,
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "conversation_id": conversation_id,
    }


def _authenticate(user_name: str, password: str) -> User:
    auth_service = AuthService()
    return auth_service.authenticate(user_name, password)
