from pydantic import BaseModel,Field
from app.schemas.user import User

class CreateUserRequest(BaseModel):
    """
    Schema for user creation request validation.
    This class defines the request schema for creating new users in the RBAC chatbot system.
    It uses Pydantic for data validation and ensures all user input meets specified requirements.
    """
    user: User = Field(description="The user details for the new user")
    
    created_by: str = Field(description="The admin creating this user")
 