
from pydantic import BaseModel

from pydantic import Field
from typing import Literal,Optional

class User(BaseModel):
    """User schema."""
    user_id: str = Field(..., description="Username")
    email: Optional[str] | None = Field(default=None, description="User email address")
    user_role:list[Literal["general", "engineering", "marketing", "finance", "hr","admin","c-level"]] = Field(...,description="Roles assigned to the user")
    password: Optional[str] | None = Field(default=None, description="User password")
    is_active: bool = Field(default=True, description="Indicates if the user is active")