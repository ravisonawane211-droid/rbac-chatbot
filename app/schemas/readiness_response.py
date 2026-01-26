from pydantic import BaseModel
from pydantic import Field

class ReadinessResponse(BaseModel):
    """Readiness check response."""

    status: str = Field(..., description="Service status")
    qdrant_connected: bool = Field(..., description="Qdrant connection status")
    collection_info: dict = Field(..., description="Collection information")