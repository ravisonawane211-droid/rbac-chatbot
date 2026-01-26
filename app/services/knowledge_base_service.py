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

        self.vector_store = vector_store or VectorStoreService()
        self.sparse_vector_store = SparseVectorService(settings.sparse_retriever_type)

        self.dense_retriever = self.vector_store.get_dense_retriever(roles=roles)

        source_docs = get_qdrant_documents()
        
        self.sparse_retriever = self.sparse_vector_store.get_sparse_retriever(docs=source_docs)

        self.hybrid_retriever = EnsembleRetriever(retrievers=[self.dense_retriever, 
                                                              self.sparse_retriever],
                                                              weights=[settings.alpha,1 - settings.alpha])
        self.logger.info("KnowledgeBaseServie initialized")

    
    def search_knowledge_base(self,question: str) -> list[Document]:

        try:
            self.logger.info(f"searching knowledge for user query: {question}")

            source_docs = self.hybrid_retriever.invoke(question)

            if settings.ENABLE_RERANKING:
                source_docs = self.rerank_docs(question=question, docs = source_docs)

            self.logger.info(f"hybrid search retriever retrived {len(source_docs)} for user_query : {question}")

            return source_docs
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


    


