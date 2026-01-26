
from pydantic import BaseModel
from pydantic import Field

class LoginRequest(BaseModel):
    """Login request schema."""

    user_name: str = Field(..., description="Username for login")
    password: str = Field(..., description="Password for login")