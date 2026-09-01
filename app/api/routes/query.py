"""Query endpoints for RAG Q&A."""

import asyncio
import time
import json

from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import StreamingResponse

from app.schemas.error_response import ErrorResponse
from app.schemas.query_request import QueryRequest
from app.schemas.query_response import QueryResponse
from app.auth.jwt_bearer import JWTBearer
from app.config.config import get_settings
from app.schemas.evaluation_request import EvaluationRequest
from app.services.chat_service import ChatService
from app.services.evaluation_service import EvaluationService
from app.services.query_pipeline_service import execute_query_pipeline
from app.utils.logger import get_logger
import threading


logger = get_logger(__name__)
router = APIRouter(prefix="/query", tags=["Query"])
settings = get_settings()
auth_scheme = JWTBearer()


@router.post(
    "",
    response_model=QueryResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Query processing error"},
    },
    summary="Ask a question",
    description="Submit a question and get an AI-generated answer based on the ingested documents.",
)
async def query(request: QueryRequest,user_info: dict=Depends(auth_scheme)) -> QueryResponse:
    """Process a RAG query."""
    logger.info(
        f"Query received: {request.question[:100]}... "
        f"(sources={request.include_sources}, eval={request.enable_evaluation})"
    )
    start_time = time.time()

    try:
        processing_time = (time.time() - start_time) * 1000

        answer, sources, _, _ = await execute_query_pipeline(
            question=request.question,
            user_info=user_info,
        )

        logger.info(f"Query processed in {processing_time:.2f}ms ")

        
        if settings.enable_evaluation:
            try:
                evaluation_service = EvaluationService()
                evaluation_request = _get_evaluation_request(
                    conversation_id=request.conversation_id,
                    question=request.question,
                    answer=answer,
                    sources=sources,
                    user_id=user_info["user_id"],
                )
                threading.Thread(
                    target=evaluation_service.send_for_evaluation,
                    args=(evaluation_request,),
                    daemon=True,
                ).start()
            except Exception:
                logger.exception("Evaluation dispatch failed; returning chat response anyway")

        return QueryResponse(
            question=request.question,
            answer=answer,
            sources=sources,
            processing_time_ms=round(processing_time, 2)
        )

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}",
        )


@router.post(
    "/stream",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Query processing error"},
    },
    summary="Ask a question (streaming)",
    description="Submit a question and get a streaming AI-generated answer.",
)
async def query_stream(request: QueryRequest,user_info: dict =Depends(auth_scheme)) -> StreamingResponse:
    """Process a RAG query with streaming response."""
    logger.info(f"Streaming query received: {request.question[:100]} by {user_info["user_id"]}")

    try:
        chat_service = ChatService(user_info=user_info)

        async def generate():
            """Generate incremental status and answer updates."""
            try:
                yield "event: progress\ndata: {\"message\": \"Thinking...\"}\n\n"
                await asyncio.sleep(0.2)

                yield "event: progress\ndata: {\"message\": \"Checking the relevant knowledge base...\"}\n\n"
                await asyncio.sleep(0.2)

                yield "event: progress\ndata: {\"message\": \"Preparing the final answer...\"}\n\n"
                await asyncio.sleep(0.1)

                result = await chat_service.chat(question=request.question, conversation_id=user_info.get("conversation_id"))
                answer = result.get("answer", "") or "No answer returned."

                for i in range(0, len(answer), 35):
                    chunk = answer[i:i+35]
                    yield f"event: chunk\ndata: {json.dumps({'text': chunk})}\n\n"
                    await asyncio.sleep(0.04)

                yield f"event: done\ndata: {json.dumps({'answer': answer, 'sources': result.get('sources', [])})}\n\n"
            except Exception as e:
                logger.error(f"Error in stream: {e}")
                yield f"event: error\ndata: {json.dumps({'detail': str(e)})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    except Exception as e:
        logger.error(f"Error setting up stream: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}",
        )
    
def _get_evaluation_request(conversation_id:str,question:str ,answer:str,sources:list, user_id:str):
    contexts = []

    get_context(sources, contexts)
    
    metadata = {
        "retriever":"hybrid",
        "k": settings.top_k,
        "llm": settings.llm_model,
        "embedding_llm": settings.embedding_model,
        "temperature": settings.llm_temperature,
        "chunk_size": settings.chunk_size,
        "chunk_overlap": settings.chunk_overlap
    }
    eval_request = EvaluationRequest(project_id = settings.app_name,environment = settings.env,
                                     request_id = conversation_id,contexts = contexts,
                                     question = question,answer = answer,
                                     metadata = metadata, eval_type=settings.eval_type,
                                     user_id = user_id
                                     )
    return eval_request

def get_context(sources, contexts):
    for source in sources:
        content = source.get("page_content", "")
        if isinstance(content, str):
            if content.strip():
                contexts.append(content)
        elif isinstance(content, list):
            contexts.extend(
                item for item in content
                if isinstance(item, str) and item.strip()
            )
