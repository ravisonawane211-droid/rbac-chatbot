from pydantic import BaseModel,Field
from typing import Literal
from app.schemas.app_config import AppConfig

class SaveConfigRequest(BaseModel):
    
    app_config:AppConfig
    user_id:str