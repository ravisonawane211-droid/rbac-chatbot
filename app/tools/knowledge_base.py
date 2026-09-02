from langchain_core.tools import tool
from app.utils.logger import get_logger
from app.services.knowledge_base_service import KnowledgeBaseServie
from functools import lru_cache
from langchain_core.documents import Document
from langgraph.types import Command
from typing import List
from app.config.config import get_settings
import json

logger = get_logger(__name__)

settings = get_settings()

@tool("knowledge_base_search", description="Search the knowledge base vector database and return relevant response")
def knowledge_base_search(question: str, roles: List[str]) -> dict:
    """
    Search the knowledge base vector database and return relevant response.

    Args:
        question: Natural language query.
        roles: role list.
    Returns:
        Context containing response from knowledge base service with access status.
    """

    logger.info("searching user query using knowledge_base_search tool")

    knowledge_base_service = KnowledgeBaseServie(roles=roles)

    result = knowledge_base_service.search_knowledge_base(question=question)
    source_docs = result.get("documents", [])
    access_denied = result.get("access_denied", False)

    logger.info(f"Tool result: access_denied={access_denied}, num_documents={len(source_docs) if source_docs else 0}")

    if access_denied:
        # Documents exist but user doesn't have permission
        permission_response = {
            "question": question, 
            "sources": [], 
            "context": "You don't have permission to access the requested information. Please contact your administrator if you believe this is an error.", 
            "access_denied": True,
            "tool": "knowledge_base",
            "status": "ACCESS_DENIED"
        }
        logger.warning(f"Returning ACCESS_DENIED response for question: {question}")
        return permission_response

    if not source_docs:
        not_found_response = {
            "question": question, 
            "sources": [], 
            "context": f"No relevant information found in the knowledge base for your search.", 
            "access_denied": False,
            "tool": "knowledge_base",
            "status": "NOT_FOUND"
        }
        logger.info(f"Returning NOT_FOUND response for question: {question}")
        return not_found_response

    context = _format_docs(docs=source_docs)

    sources = json.dumps([
                    {"page_content": d.page_content, "metadata": d.metadata}
                    for d in source_docs
                ])

    rag_response = {
          "question": question,
          "sources": sources,
          "context": context,
          "access_denied": False,
          "tool": "knowledge_base",
          "status": "SUCCESS"
    }

    logger.info(f"received response in knowledge_base_search tool: {context[:200]}")

    return rag_response


def _format_docs(docs: list[Document]) -> str:
    """Format documents into a single context string.

    Args:
        docs: List of Document objects

    Returns:
        Formatted context string
    """
    return "\n".join("content: "+ doc.page_content+ "\n source: "+doc.metadata["source"] + "\n" for doc in docs)