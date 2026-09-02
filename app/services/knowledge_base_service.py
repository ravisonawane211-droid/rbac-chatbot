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

        self.source_docs = get_qdrant_documents()
        self.logger.info(f"Total documents in knowledge base: {len(self.source_docs)}")

        if roles and "c-level" not in roles:
            allowed_roles = list(set(roles + ["general"]))
            self.logger.info(f"Filtering for roles: {allowed_roles}")
            filtered_docs = [doc for doc in self.source_docs if doc.metadata.get("role", []) and any(role in doc.metadata["role"] for role in allowed_roles)]
            self.logger.info(f"Documents after role filtering: {len(filtered_docs)}")
        else:
            self.logger.info(f"No role filtering (c-level or empty roles)")

        dense_retriever = self.vector_store.get_dense_retriever(roles=roles)
        weights.append(settings.alpha)

        retrievers.append(dense_retriever)

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
            self.logger.info(f"[SEARCH START] User roles: {self.roles}, Question: {question[:80]}")

            # First, do the role-filtered search
            source_docs = self.hybrid_retriever.invoke(question)
            self.logger.info(f"[ROLE-FILTERED SEARCH] Returned {len(source_docs) if source_docs else 0} documents")
            
            # If no docs found with role filtering, check if docs exist via unrestricted search
            access_denied = False
            if not source_docs and self.roles and "c-level" not in self.roles:
                self.logger.info(f"[ACCESS CHECK] No documents in role-filtered search. Checking unrestricted search...")
                
                # Check if dense search would find documents without role filtering
                unrestricted_dense_retriever = self.vector_store.get_dense_retriever(roles=[])
                unrestricted_dense_docs = unrestricted_dense_retriever.invoke(question)
                self.logger.info(f"[UNRESTRICTED DENSE] Found {len(unrestricted_dense_docs) if unrestricted_dense_docs else 0} documents")
                
                unrestricted_sparse_docs = []
                # Check if sparse (BM25) search would find documents without role filtering
                if self.source_docs:
                    unrestricted_sparse_retriever = self.sparse_vector_store.get_sparse_retriever(docs=self.source_docs, roles=[])
                    unrestricted_sparse_docs = unrestricted_sparse_retriever.invoke(question)
                    self.logger.info(f"[UNRESTRICTED SPARSE] Found {len(unrestricted_sparse_docs) if unrestricted_sparse_docs else 0} documents")
                
                # If either retriever finds documents, user is denied access due to role restrictions
                if unrestricted_dense_docs or unrestricted_sparse_docs:
                    access_denied = True
                    self.logger.warning(f"[ACCESS DENIED] Documents exist but user role {self.roles} lacks permission")
                else:
                    self.logger.info(f"[NO RESULTS] No documents found even in unrestricted search")

            if not source_docs:
                self.logger.info(f"[RETURN] Empty documents. access_denied={access_denied}")
                return {"documents": [], "access_denied": access_denied}

            # Log the roles of returned documents for debugging
            doc_roles = []
            for doc in source_docs:
                doc_roles.append(doc.metadata.get("role", []))
            self.logger.info(f"[DOC ROLES] Returned documents have roles: {doc_roles[:5]}")  # Log first 5

            if settings.ENABLE_RERANKING:
                source_docs = self.rerank_docs(question=question, docs=source_docs)

            self.logger.info(f"[RETURN] Found {len(source_docs)} documents. access_denied=False")

            return {"documents": source_docs, "access_denied": False}
        except Exception as e:
            self.logger.error(f"[ERROR] Exception in search_knowledge_base: {str(e)}", exc_info=True)
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


    


