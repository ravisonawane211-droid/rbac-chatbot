from app.utils.logger import get_logger
from app.services.dense_vector_store_service import VectorStoreService
from functools import lru_cache
from langchain_core.documents import Document
from app.config.config import get_settings
from app.services.sparse_vector_service import SparseVectorService
from langchain_classic.retrievers.ensemble import EnsembleRetriever
from langchain_cohere.rerank import CohereRerank
from app.utils.util import reciprocal_rank_fusion


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
        retrievers = []
        weights = []

        self.source_docs = get_qdrant_documents()
        self.logger.info(f"Total documents in knowledge base: {len(self.source_docs)}")

        self.unrestricted_dense_retriever = self.vector_store.get_dense_retriever(roles=[])
        self.unrestricted_sparse_retriever = self.sparse_vector_store.get_sparse_retriever(docs=self.source_docs, roles=[])

        if roles and "c-level" not in roles:
            allowed_roles = list(set(roles + ["general"]))
            self.logger.info(f"Filtering for roles: {allowed_roles}")
            filtered_docs = [doc for doc in self.source_docs if doc.metadata.get("role", []) and any(role in doc.metadata["role"] for role in allowed_roles)]
            self.logger.info(f"Documents after role filtering: {len(filtered_docs)}")
        else:
            self.logger.info("No role filtering (c-level or empty roles)")

        self.dense_retriever = self.vector_store.get_dense_retriever(roles=roles)

        if filtered_docs:
            self.sparse_retriever = self.sparse_vector_store.get_sparse_retriever(docs=filtered_docs, roles=roles)
        else:
            self.sparse_retriever = self.unrestricted_sparse_retriever

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

            filtered_dense_docs = self.dense_retriever.invoke(question)
            filtered_sparse_docs = self.sparse_retriever.invoke(question) if hasattr(self, "sparse_retriever") else []

            self.logger.info(
                f"[ROLE-FILTERED SEARCH] Dense results: {len(filtered_dense_docs) if filtered_dense_docs else 0}; "
                f"Sparse results: {len(filtered_sparse_docs) if filtered_sparse_docs else 0}"
            )

            unrestricted_dense_docs = self.unrestricted_dense_retriever.invoke(question)
            unrestricted_sparse_docs = self.unrestricted_sparse_retriever.invoke(question)
            self.logger.info(
                f"[UNRESTRICTED SEARCH] Dense results: {len(unrestricted_dense_docs) if unrestricted_dense_docs else 0}; "
                f"Sparse results: {len(unrestricted_sparse_docs) if unrestricted_sparse_docs else 0}"
            )

            access_denied = False
            if self.roles and "c-level" not in self.roles:
                allowed_roles = set(self.roles + ["general"])

                def normalize_roles(doc_roles):
                    if not doc_roles:
                        return set()
                    if isinstance(doc_roles, str):
                        return {doc_roles.lower()}
                    return {str(role).lower() for role in doc_roles if role}

                unrestricted_roles = set()
                for doc in (unrestricted_dense_docs or []) + (unrestricted_sparse_docs or []):
                    unrestricted_roles.update(normalize_roles(doc.metadata.get("role", [])))

                restricted_roles = unrestricted_roles - allowed_roles
                if restricted_roles:
                    access_denied = True
                    self.logger.warning(
                        f"[ACCESS DENIED] User role {self.roles} is not allowed to access roles {sorted(restricted_roles)} for question: {question}"
                    )

            if access_denied:
                self.logger.info(f"[RETURN] Restricted documents exist; denying access. access_denied={access_denied}")
                return {"documents": [], "access_denied": True}

            results_dict = {
                "dense": filtered_dense_docs,
                "sparse": filtered_sparse_docs,
            }
            weights = {"dense": settings.alpha, "sparse": 1 - settings.alpha}
            source_docs = reciprocal_rank_fusion(results_dict, weights, top_n=settings.top_k)

            if not source_docs:
                self.logger.info(f"[RETURN] Empty documents. access_denied={access_denied}")
                return {"documents": [], "access_denied": access_denied}

            if settings.ENABLE_RERANKING:
                source_docs = self.rerank_docs(question=question, docs=source_docs)

            self.logger.info(f"[RETURN] Found {len(source_docs)} documents. access_denied={access_denied}")
            return {"documents": source_docs, "access_denied": access_denied}
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


    


