
from pydantic import BaseModel
from fastapi import UploadFile
from typing import Literal

class DocumentUploadRequest(BaseModel):
    """
    DocumentUploadRequest schema for handling document upload requests.
    Attributes:
        file (UploadFile): The file to be uploaded.
        role (Literal["general", "engineering", "marketing", "finance", "hr"]): The role of the user uploading the file.
    """

    file: UploadFile
    role: Literal["general", "engineering", "marketing", "finance", "hr"]