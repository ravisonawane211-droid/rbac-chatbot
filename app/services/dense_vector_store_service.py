"""Vector store module for Qdrant operations."""

from functools import lru_cache
from typing import Any
from uuid import uuid4

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.config.config import get_settings
from app.services.embedding_service import get_embeddings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Embedding dimension for text-embedding-3-small
EMBEDDING_DIMENSION = 1536

@lru_cache
def get_qdrant_client() -> QdrantVectorStore:
    """Get cached Qdrant client instance.

    Returns:
        Configured QdrantVectorStore instance
    """
    logger.info(f"Connecting to Qdrant at: {settings.qdrant_path}")
    embeddings = get_embeddings()
    vector_store = QdrantVectorStore.from_documents(
                collection_name=settings.collection_name,
                embedding= embeddings,
                path=settings.qdrant_path,
                documents=[]
            )
        
    logger.info("Qdrant vector_store connected successfully")
    return vector_store


class VectorStoreService:
    """Service for managing vector store operations."""

    def __init__(self, collection_name: str | None = None):
        """Initialize vector store service.

        Args:
            collection_name: Name of the Qdrant collection (default from settings)
        """
        self.collection_name = collection_name or settings.collection_name
        # self.client = get_qdrant_client()

        #self.embeddings = get_embeddings()

        # Ensure collection exists
        # self._ensure_collection()

        # Create Index
        # self.client.create_payload_index(
        #     collection_name=settings.collection_name,
        #     field_name="role",
        #     field_schema=PayloadSchemaType.KEYWORD)


        # Initialize LangChain Qdrant vector store
        self.vector_store = get_qdrant_client()

        logger.info(f"VectorStoreService initialized for collection: {self.collection_name}")

    def _ensure_collection(self) -> None:
        """Ensure the collection exists, create if not."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(
                f"Collection '{self.collection_name}' exists with "
                f"{collection_info.points_count} points"
            )
        except UnexpectedResponse:
            logger.info(f"Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")

    def add_documents(self, documents: list[Document]) -> list[str]:
        """Add documents to the vector store.

        Args:
            documents: List of Document objects to add

        Returns:
            List of document IDs
        """
        if not documents:
            logger.warning("No documents to add")
            return []

        logger.info(f"Adding {len(documents)} documents to collection")

        # Generate unique IDs for each document
        ids = [str(uuid4()) for _ in documents]

        # Add to vector store
        self.vector_store.add_documents(documents, ids=ids)

        logger.info(f"Successfully added {len(documents)} documents")
        return ids

    def search(
        self,
        query: str,
        k: int | None = None,
    ) -> list[Document]:
        """Search for similar documents.

        Args:
            query: Search query
            k: Number of results to return (default from settings)

        Returns:
            List of similar Document objects
        """
        k = k or settings.top_k
        logger.debug(f"Searching for: {query[:50]}... (k={k})")

        results = self.vector_store.similarity_search(query, k=k)

        logger.debug(f"Found {len(results)} results")
        return results

    def search_with_scores(
        self,
        query: str,
        k: int | None = None,
    ) -> list[tuple[Document, float]]:
        """Search for similar documents with relevance scores.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of (Document, score) tuples
        """
        k = k or settings.top_k
        logger.debug(f"Searching with scores for: {query[:50]}... (k={k})")

        results = self.vector_store.similarity_search_with_score(query, k=k)

        logger.debug(f"Found {len(results)} results with scores")
        return results

    def get_dense_retriever(self, k: int | None = None, roles: list[str] = []) -> Any:
        """Get a retriever for the vector store.

        Args:
            k: Number of documents to retrieve

        Returns:
            LangChain retriever object
        """
        logger.info("retriving documents using retriever")

        k = k or settings.top_k
        
        if roles and "c-level" not in roles:
            allowed_roles = list(set(roles + ["general"]))
            qdrant_filter = Filter(
                should=[
                    FieldCondition(
                        key="metadata.role",
                        match=MatchValue(value=role)
                    )
                    for role in allowed_roles
                ]
            )
            retriever = self.vector_store.as_retriever(
            search_type="similarity",
            k = k,
            filter = qdrant_filter
            )
            retriever._get_relevant_documents
        else:
            retriever = self.vector_store.as_retriever(
            search_type="similarity",
            k = k)

        return retriever

    def delete_collection(self) -> None:
        """Delete the entire collection."""
        logger.warning(f"Deleting collection: {self.collection_name}")
        self.client.delete_collection(self.collection_name)
        logger.info(f"Collection '{self.collection_name}' deleted")

    def get_collection_info(self) -> dict:
        """Get information about the collection.

        Returns:
            Dictionary with collection statistics
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "indexed_vectors_count": info.indexed_vectors_count,
                "status": info.status.value,
            }
        except UnexpectedResponse:
            return {
                "name": self.collection_name,
                "points_count": 0,
                "indexed_vectors_count": 0,
                "status": "not_found",
            }

    def health_check(self) -> bool:
        """Check if vector store is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Vector store health check failed: {e}")
            return False
