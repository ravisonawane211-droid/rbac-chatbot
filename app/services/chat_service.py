from app.services.dense_vector_store_service import VectorStoreService
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.config.config import get_settings
from app.prompts.prompts import RAG_PROMPT
from app.utils.util import format_docs
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.utils.logger import get_logger
from app.services.sparse_vector_service import SparseVectorService
from langchain_classic.retrievers.ensemble import EnsembleRetriever
from functools import lru_cache
from langchain_core.documents import Document
from app.agents.fin_solve_agent import fin_solve_agent
import json

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



class ChatService:
    def __init__(self, vector_store: VectorStoreService | None = None, roles:list[str]=[]):
        self.logger = get_logger(__name__)

        self.roles = roles
        self.vector_store = vector_store or VectorStoreService()
        self.sparse_vector_store = SparseVectorService(settings.sparse_retriever_type)

        self.dense_retriever = self.vector_store.get_dense_retriever(roles=roles)

        source_docs = get_qdrant_documents()
        
        self.sparse_retriever = self.sparse_vector_store.get_sparse_retriever(docs=source_docs)

        self.hybrid_retriever = EnsembleRetriever(retrievers=[self.dense_retriever, 
                                                              self.sparse_retriever],
                                                              weights=[settings.alpha,1 - settings.alpha])
        self.llm = ChatGoogleGenerativeAI(model=settings.llm_model,
                                          temperature=settings.llm_temperature)
          # Create prompt template
        self.prompt = ChatPromptTemplate.from_template(RAG_PROMPT)

        # Build LCEL chain
        self.chain = (
            {
                "context": self.hybrid_retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        self.logger.info(
            f"RAGChain initialized with model={settings.llm_model}, "
            f"retrieval_k={settings.top_k}"
        )

    async def aquery_with_sources(self, question: str) -> dict:
        """Execute an async RAG query and return sources.

        Args:
            question: User question

        Returns:
            Dictionary with answer and source documents
        """
        self.logger.info(f"Processing async query with sources: {question[:100]}...")

        try:
            # dense_docs = self.dense_retriever.invoke(question)

            # sparse_docs = self.sparse_retriever.invoke(question)

            # ranked_docs = reciprocal_rank_fusion(results_dict={"bm25": sparse_docs, "dense": dense_docs},
            #  weights={"bm25": 0.3, "dense": 0.7})

            # Get answer
            answer = await self.chain.ainvoke(question)

            # Get source documents (sync operation)
            source_docs = self.hybrid_retriever.invoke(question)

            self.logger.info(f"Async query processed with {len(source_docs)} sources")

            return {
                "answer": answer,
                "sources": source_docs,
            }
        except Exception as e:
            self.logger.error(f"Error processing async query with sources: {e}")
            raise
    

    async def chat(self,question: str,conversation_id:str):
        try:
            self.logger.info(f"invoking agent to answer user query : {question} with role: {self.roles}")
            
            answer = ""

            config = {"configurable": {"thread_id": conversation_id}}

            response = await fin_solve_agent.ainvoke(input={"messages":[{"role": "user", "content": question}],
                                                            "rag_response":{}},
                                    context={"question": question,"roles": self.roles},
                                    config=config)
            
            if response:
                answer = response["messages"][-1].text

                knowledgge_base_resp = self.extract_tool(messages=response["messages"] , tool_name="knowledge_base_search")

                text_to_sql_resp = self.extract_tool(messages=response["messages"] , tool_name="text_to_sql")

                # source_docs = self.hybrid_retriever.invoke(question)

            self.logger.info(f"received response from agent: {answer} for user query: {question}")

            return {
                    "answer": answer,
                    "knowledgge_base_resp": knowledgge_base_resp,
                    "text_to_sql_resp": text_to_sql_resp
                }
            
        except Exception as e:
            self.logger.error(f"error while invoking agent : {e}")
            raise e

    def extract_tool(self, messages, tool_name):
        for m in messages:
            if m.type == "tool" and m.name == tool_name:
                return json.loads(m.content)



        

