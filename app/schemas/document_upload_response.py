
from pydantic import BaseModel
from pydantic import Field

class DocumentUploadResponse(BaseModel):
    """
    DocumentUploadResponser represents the response schema for a document upload operation.
    Attributes:
        message (str): Status message indicating the result of the upload operation.
        filename (str): The name of the uploaded file.
        chunks_created (int): The number of chunks created from the uploaded document.
        document_ids (list[str]): A list of unique identifiers for the created document chunks.
    """
    message: str = Field(..., description="Status message")
    filename: str = Field(..., description="Uploaded filename")
    chunks_created: int = Field(..., description="Number of chunks created")
    document_ids: list[str] | None = Field(..., description="List of document IDs")