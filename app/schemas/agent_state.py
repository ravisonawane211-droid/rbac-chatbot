from pydantic import Field , BaseModel 
from typing import List


class AgentState(BaseModel):
    question: str = Field(..., description="Question provided by user")
    roles: List[str] = Field(..., description="Logged-in user roles")
