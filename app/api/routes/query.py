"""Query endpoints for RAG Q&A."""

import time

from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import StreamingResponse

from app.schemas.error_response import ErrorResponse
from app.schemas.query_request import QueryRequest
from app.schemas.query_response import QueryResponse
from app.services.chat_service import ChatService
from app.auth.jwt_bearer import JWTBearer
from app.utils.logger import get_logger
from app.services.evaluation_service import EvaluationService
from app.schemas.evaluation_request import EvaluationRequest
from app.services.query_cache_service import QueryCacheService
from app.config.config import get_settings
import threading
import json
from langchain_core.documents import Document


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

        chat_service = ChatService(roles = user_info["roles"])
        #result = await chat_service.aquery_with_sources(request.question)

        query_cache_service = QueryCacheService(
            redis_url=settings.REDIS_REST_URL,
            redis_token=settings.REDIS_REST_TOKEN
        )

        if query_cache_service and query_cache_service.enabled:
            cache_key = query_cache_service.get_key(request.question, role=user_info["roles"][0])
            cached_result = query_cache_service.get(cache_key, cache_type="rag")

            if cached_result:
                logger.info(f"Cache HIT {cached_result} for question: '{request.question[:50]}...'")
                answer = cached_result["answer"]
                sources = cached_result["sources"]
                sources = json.loads(sources)
                
                sources = [
                    Document(page_content=d["page_content"], metadata=d["metadata"])
                    for d in sources
                ]
            else:
                result = await chat_service.chat(question=request.question)

                answer = result["answer"]
                sources = result["sources"]

                payload = json.dumps([
                    {"page_content": d.page_content, "metadata": d.metadata}
                    for d in sources
                ])

                result = {
                "question": request.question,
                "answer": answer,
                "chunks_used": len(sources),
                "sources": payload,
                "model": settings.llm_model,
                }
                ttl = settings.CACHE_TTL_RAG  # Default: 1 hour
                query_cache_service.set(cache_key, result, ttl=ttl, cache_type="rag")
                logger.info(f"Cache MISS - cached result for '{request.question[:50]}...' (TTL: {ttl}s)")
        else:
            result = await chat_service.chat(question=request.question)

            answer = result["answer"]
            sources = result["sources"]


        logger.info(
            f"Query processed in {processing_time:.2f}ms "
        )

        #app_config = get_app_config()

        #logger.info(f"retrived app config : {app_config}")

        #if app_config.enable_eval == "Yes":
        if request.enable_evaluation:
            evaluation_service = EvaluationService()

            evaluation_request = _get_evaluation_request(conversation_id=request.conversation_id,
                                    question=request.question,answer=answer,sources=sources)
            
            threading.Thread(
                target=evaluation_service.send_for_evaluation,
                args=(evaluation_request,),
                daemon=True
            ).start()

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
        chat_service = ChatService(roles=user_info["roles"])

        async def generate():
            """Generate streaming response."""
            try:
                for chunk in chat_service.aquery_with_sources(request.question):
                    yield chunk
            except Exception as e:
                logger.error(f"Error in stream: {e}")
                yield f"\n\nError: {str(e)}"

        return StreamingResponse(
            generate(),
            media_type="text/plain",
        )

    except Exception as e:
        logger.error(f"Error setting up stream: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}",
        )
    
def _get_evaluation_request(conversation_id:str,question:str ,answer:str,sources:list):
    contexts = [source.page_content for source in sources]
    
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
                                     metadata = metadata, eval_type="Ragas"
                                     )
    return eval_request
