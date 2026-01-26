from langchain_community.retrievers import BM25Retriever
from app.utils.logger import get_logger

logger = get_logger(__name__)

class SparseVectorService:
    def __init__(self,sparse_retriever_type):
        self.sparse_retriever_type = sparse_retriever_type
        logger.info(f"SparseVectorService initialized for retriever type: {self.sparse_retriever_type}")
        

    def get_sparse_retriever(self,docs):
        
        logger.info(f"getting sparse retriver for type {self.sparse_retriever_type} ")
        if self.sparse_retriever_type == "BM25":
            sparse_retriver = BM25Retriever.from_documents(documents= docs)
        return sparse_retriver
