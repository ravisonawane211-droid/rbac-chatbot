from pydantic import BaseModel
from typing_extensions import Literal


class SaveConfigResponse(BaseModel):
    message: str
    status: Literal["success", "failure"]