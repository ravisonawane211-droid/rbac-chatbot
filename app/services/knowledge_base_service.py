from app.utils.logger import get_logger
from app.services.dense_vector_store_service import VectorStoreService
from functools import lru_cache
from langchain_core.documents import Document
from app.config.config import get_settings
from app.services.sparse_vector_service import SparseVectorService
from langchain_classic.retrievers.ensemble import EnsembleRetriever
from langchain_cohere.rerank import CohereRerank


settings = get_settings()


@lru_cache
def get_qdrant_documents():
    vector_store = VectorStoreService()
    client = vector_store.vector_store.client
    collection_name = vector_store.collection_name
    all_docs = []
    offset = None

    while True:
        points, offset = client.scroll(
            collection_name=collection_name,
            limit=100,
            with_payload=True,
            with_vectors=False
        )
        points[0]
        all_docs = [Document(page_content=point.payload["page_content"],
                             metadata=point.payload["metadata"]) for point in points]
        all_docs.extend(all_docs)

        if offset is None:
            break
    return all_docs

class KnowledgeBaseServie:

    def __init__(self,vector_store: VectorStoreService | None = None, roles:list[str]=[]):
        self.logger = get_logger(__name__)

        self.roles = roles
        self.vector_store = vector_store or VectorStoreService()
        self.sparse_vector_store = SparseVectorService(settings.sparse_retriever_type)

        filtered_docs = []
        retrievers= []
        weights = []

        source_docs = get_qdrant_documents()

        # Store unrestricted retrievers for access denial detection
        self.unrestricted_dense_retriever = self.vector_store.get_dense_retriever(roles=[])

        if roles and "c-level" not in roles:
            allowed_roles = list(set(roles + ["general"]))
            filtered_docs = [doc for doc in source_docs if doc.metadata.get("role", []) and any(role in doc.metadata["role"] for role in allowed_roles)]

        dense_retriever = self.vector_store.get_dense_retriever(roles=roles)
        weights.append(settings.alpha)

        retrievers.append(dense_retriever)

        # Store unrestricted sparse retriever for access denial detection
        if source_docs:
            self.unrestricted_sparse_retriever = self.sparse_vector_store.get_sparse_retriever(docs=source_docs, roles=[])
        else:
            self.unrestricted_sparse_retriever = None

        if filtered_docs:
            sparse_retriever = self.sparse_vector_store.get_sparse_retriever(docs=filtered_docs, roles=roles)
            retrievers.append(sparse_retriever)
            weights.append(1 - settings.alpha)

        self.hybrid_retriever = EnsembleRetriever(retrievers=retrievers,
                                                              weights=weights)
        self.logger.info("KnowledgeBaseServie initialized")

    
    def search_knowledge_base(self,question: str) -> dict:
        """
        Search knowledge base and return documents with access status.
        
        Returns:
            dict with keys:
                - documents: List of accessible documents
                - access_denied: bool indicating if documents exist but are inaccessible due to RBAC
        """

        try:
            self.logger.info(f"searching knowledge for user query: {question}")

            source_docs = self.hybrid_retriever.invoke(question)
            
            # If no docs found with role filtering, check if docs exist via unrestricted retrievers
            access_denied = False
            if not source_docs and self.roles and "c-level" not in self.roles:
                # Check if dense search would find documents without role filtering
                unrestricted_dense_docs = self.unrestricted_dense_retriever.invoke(question)
                unrestricted_sparse_docs = []
                
                # Check if sparse (BM25) search would find documents without role filtering
                if self.unrestricted_sparse_retriever:
                    unrestricted_sparse_docs = self.unrestricted_sparse_retriever.invoke(question)
                
                # If either retriever finds documents, user is denied access due to role restrictions
                if unrestricted_dense_docs or unrestricted_sparse_docs:
                    access_denied = True
                    self.logger.info(f"Access denied: Documents exist but user role {self.roles} does not have permission for question: {question}")

            if not source_docs:
                self.logger.info(f"No accessible documents found for question: {question} with your role: {self.roles}")
                return {"documents": [], "access_denied": access_denied}

            if settings.ENABLE_RERANKING:
                source_docs = self.rerank_docs(question=question, docs=source_docs)

            self.logger.info(f"hybrid search retriever retrived {len(source_docs)} for user_query : {question}")

            return {"documents": source_docs, "access_denied": False}
        except Exception as e:
            self.logger.error("Error occurred while searching knowledge base")
            raise e
        
    
    def rerank_docs(self, question, docs) -> list[Document]:
        
        try:
            self.logger.info(f"re-ranking documents for user query: {question}")

            cohere_re_ranker = CohereRerank(cohere_api_key=settings.COHERE_API_KEY,
                                            model=settings.RERANK_MODEL,
                                            top_n=settings.COHERE_TOP_N)
            
            re_ranked_docs = cohere_re_ranker.compress_documents(documents=docs, query=question)

            self.logger.info(f"re-ranking documents completed for user query: {question} , re-ranked docs: {len(re_ranked_docs)}")

            return re_ranked_docs
        except Exception as e:
            self.logger.error("Error occurred while re-ranking documents")
            raise e


    


