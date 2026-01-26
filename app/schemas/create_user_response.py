
from pydantic import BaseModel
from typing import Literal

class CreateUserResponse(BaseModel):
    """
    CreateUserResponse is a Pydantic model that represents the response structure 
    for creating a user in the system.
    Attributes:
        message (str): A descriptive message about the result of the user creation process.
        status (Literal["success", "failure"]): The status of the user creation operation, 
            indicating whether it was successful or failed.
        user_name (str): The username of the created user.
        user_role (Literal["general", "engineering", "marketing", "finance", "hr", "admin"]): 
            The role assigned to the created user, which determines their permissions and access 
            within the system.
    """

    message: str
    status: Literal["success", "failure"]
    user_name: str
    user_role: Literal["general", "engineering", "marketing", "finance", "hr","admin","c-level"]

