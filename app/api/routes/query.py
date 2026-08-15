"""Query endpoints for RAG Q&A."""

import asyncio
import time
import json

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

        chat_service = ChatService(user_info = user_info)
        #result = await chat_service.aquery_with_sources(request.question)

        query_cache_service = QueryCacheService(
            redis_url=settings.REDIS_REST_URL,
            redis_token=settings.REDIS_REST_TOKEN
        )

        if query_cache_service and query_cache_service.enabled:
            cache_key = query_cache_service.get_key(request.question, role=user_info["roles"][0])
            cached_result = query_cache_service.get(cache_key, cache_type="rag")
            sources = []
            if cached_result:
                logger.info(f"Cache HIT {cached_result} for question: '{request.question[:50]}...'")
                answer = cached_result.get("answer","")
                sources = cached_result.get("sources",[])
                sql_result = cached_result.get("sql_result","")
                
                # if sources:
                #     sources = json.loads(sources)
                    # sources = [
                    #             Document(page_content=d["page_content"], metadata=d["metadata"])
                    #             for d in sources
                    #           ]
                if sql_result:
                    sources.extend([{"page_content":sql_result}])
            else:
                result = await chat_service.chat(question=request.question, conversation_id=user_info["conversation_id"])

                answer = result["answer"]
                knowledgge_base_resp = result["knowledgge_base_resp"]
                text_to_sql_resp = result["text_to_sql_resp"]
                
                cache_result = {}
                sources = []
                logger.info(f"caching query response in cache..")
                cache_result["question"] = request.question
                cache_result["answer"] = answer

                if knowledgge_base_resp:
                    sources = knowledgge_base_resp["sources"]
                    sources = json.loads(sources)

                    cache_result = {
                        **cache_result,
                        "chunks_used": len(sources),
                        "sources": sources,
                        "model": settings.llm_model,
                        "tool": knowledgge_base_resp["tool"]
                    }
                   

                if text_to_sql_resp:
                    cache_result["sql_query"] = text_to_sql_resp["sql_query"]
                    cache_result["sql_result"] = text_to_sql_resp["results"]
                    cache_result["row_count"] = text_to_sql_resp["row_count"]
                    sources.extend([{"page_content":cache_result["sql_result"]}])
                
                ttl = settings.CACHE_TTL_RAG  # Default: 1 hour
                query_cache_service.set(cache_key, cache_result, ttl=ttl, cache_type="rag")

                logger.info(f"Cache MISS - cached result for '{request.question[:50]}...' (TTL: {ttl}s)")
        else:
            result = await chat_service.chat(question=request.question, conversation_id=user_info["conversation_id"])

            answer = result.get("answer", "")
            sources = result.get("sources", [])


        logger.info(
            f"Query processed in {processing_time:.2f}ms "
        )

        
        if settings.enable_evaluation:
            evaluation_service = EvaluationService()

            evaluation_request = _get_evaluation_request(conversation_id=request.conversation_id,
                                    question=request.question,answer=answer,sources=sources, user_id=user_info["user_id"])
            
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
    contexts = [source.get("page_content","") for source in sources]
    
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
