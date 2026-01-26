from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """Request for RAG query."""

    question: str = Field(
        ...,
        description="Question to ask",
        min_length=1,
        max_length=1000,
    )
    include_sources: bool = Field(
        default=True,
        description="Include source documents in response",
    )
    enable_evaluation: bool = Field(
        default=False,
        description="Enable RAGAS evaluation (faithfulness, answer relevancy)",
    )

    user_name: str | None = Field(default=None, min_length=4, description="User name for RBAC")

    conversation_id:str = Field(...,description="Conversation_Id for authenticated users during Q/A interaction.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "What is RAG?",
                    "include_sources": True,
                    "enable_evaluation": False,
                    "user_name": "Test",
                    "conversation_id":"abc123"
                }
            ]
        }
    }