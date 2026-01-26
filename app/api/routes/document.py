"""Document management endpoints."""

from fastapi import APIRouter, Depends, UploadFile, HTTPException

from app.schemas.document_upload_response import DocumentUploadResponse
from app.schemas.error_response import ErrorResponse
from app.services.document_process_service import DocumentProcessService
from app.services.dense_vector_store_service import VectorStoreService
from app.services.db_service import DatabaseService
from app.auth.jwt_bearer import JWTBearer
from app.utils.logger import get_logger
from pathlib import Path
from app.config.config import get_settings
import pandas as pd
import uuid

logger = get_logger(__name__)
router = APIRouter(prefix="/documents", tags=["Documents"])
settings = get_settings()
auth_scheme = JWTBearer()


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file type"},
        500: {"model": ErrorResponse, "description": "Processing error"},
    },
    summary="Upload and ingest a document",
    description="Upload a document (PDF, TXT, or CSV) to be processed and added to the vector store.",
)
async def upload_document(
    file: UploadFile,
    role: str,
    user_info: dict =Depends(auth_scheme)
) -> DocumentUploadResponse:
    """Upload and process a document."""
    file = file
    logger.info(f"Received document upload: {file.filename} by {user_info["user_id"]}")

    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    try:
        # Process document
        processor = DocumentProcessService()
        documents = processor.process_upload(file.file, file.filename)
        file_path = Path(file.filename)
        extension = file_path.suffix.lower()

        if extension != ".csv":
            
            if not documents:
                raise HTTPException(
                    status_code=400,
                    detail="No content could be extracted from the document",
                )

            # update metadata with user role
            for chunk in documents:
                
                chunk.metadata = {
                    "role": role.lower(),
                    "source": file.filename,
                    "id": uuid.uuid4().hex,
                    **chunk.metadata
                }
                
            # Add to vector store
            vector_store = VectorStoreService()
            document_ids = vector_store.add_documents(documents)

            logger.info(
                f"Successfully processed {file.filename}: "
                f"{len(documents)} chunks, {len(document_ids)} documents"
            )
        else:
            db_service = DatabaseService()
            table_name = file.filename.split(".")[0].lower()

            df_table_metadata = pd.DataFrame([{"role": role.lower(), "table_name": table_name}])
            db_service.save_dataframe_to_table(df=df_table_metadata, table_name="table_access_metadata")

            db_service.save_dataframe_to_table(df=documents, table_name=table_name)

            document_ids = None

            logger.info(
                f"Successfully processed {file.filename}: ")

        return DocumentUploadResponse(
            message="Document uploaded and processed successfully",
            filename=file.filename,
            chunks_created=len(documents),
            document_ids=document_ids,
        )
    except ValueError as e:
        logger.warning(f"Invalid file upload: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}",
        )


@router.delete(
    "/collection",
    responses={
        200: {"description": "Collection deleted successfully"},
        500: {"model": ErrorResponse, "description": "Deletion error"},
    },
    summary="Delete the entire collection",
    description="Delete all documents from the vector store. Use with caution!",
)
async def delete_collection() -> dict:
    """Delete the entire document collection."""
    logger.warning("Collection deletion requested")

    try:
        vector_store = VectorStoreService()
        vector_store.delete_collection()

        return {"message": "Collection deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting collection: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting collection: {str(e)}",
        )
