from pydantic import BaseModel
from pydantic import Field
from user import User
from typing import Literal

class UserListResponse(BaseModel):
    """User list response schema."""

    users: list[User] = Field(..., description="List of user details")
    status: Literal["success", "failure"] = Field(..., description="The status of the user list retrieval")
    message: str = Field(..., description="Response message regarding the user list retrieval")