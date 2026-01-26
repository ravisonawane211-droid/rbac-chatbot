
from pydantic import BaseModel

from pydantic import Field
from typing import Literal
from app.schemas.user import User

class LoginResponse(BaseModel):
    """Login response schema."""

    message: str = Field(..., description="Login response message")
    status: Literal["success", "failure"] = Field(..., description="The login status of the user")
    user: User = Field(description="The logged-in user details")
    access_token: str = Field(..., description="JWT access token for authenticated requests")
    conversation_id:str = Field(...,description="Conversation_Id for authenticated users during Q/A interaction.")