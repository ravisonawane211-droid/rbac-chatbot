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
        Context containing response from knowledge base service.
    """

    logger.info("searching user query using knowledge_base_search tool")

    knowledge_base_service = KnowledgeBaseServie(roles=roles)

    source_docs = knowledge_base_service.search_knowledge_base(question=question)

    context = _format_docs(docs=source_docs)

    sources = json.dumps([
                    {"page_content": d.page_content, "metadata": d.metadata}
                    for d in source_docs
                ])

    rag_response = {
          "question": question,
          "sources": sources,
          "context": context, 
          "tool": "knowledge_base"
    }

    logger.info(f"received response in knowledge_base_search tool: {context[:200]}")

    return  rag_response


def _format_docs(docs: list[Document]) -> str:
        """Format documents into a single context string.

        Args:
            docs: List of Document objects

        Returns:
            Formatted context string
        """
        return "\n".join("content: "+ doc.page_content+ "\n source: "+doc.metadata["source"] + "\n" for doc in docs)