import json

from app.agents.fin_solve_agent import fin_solve_agent
from app.config.config import get_settings
from app.utils.langfuse_tracing import build_langchain_config
from app.utils.logger import get_logger
from app.utils.util import set_current_user

settings = get_settings()


class ChatService:
    def __init__(self, user_info: dict | None = None):
        self.logger = get_logger(__name__)
        self.user_info = user_info or {}
        self.roles = self.user_info.get("roles", [])
        self.logger.info(f"ChatService initialized with roles: {self.roles}")

    async def chat(self, question: str, conversation_id: str):
        try:
            self.logger.info(f"Invoking agent to answer user query: {question} with role: {self.roles}")

            config = build_langchain_config(
                user_info=self.user_info,
                route="/chat",
                model=settings.llm_model,
                base_config={"configurable": {"thread_id": conversation_id}},
            )

            set_current_user(self.user_info)

            response = await fin_solve_agent.ainvoke(
                input={"messages": [{"role": "user", "content": question}], "rag_response": {}},
                context={"question": question, "user_info": self.user_info},
                config=config,
            )

            answer = ""
            status = None
            knowledgge_base_resp = None
            text_to_sql_resp = None

            if response:
                answer = response["messages"][-1].text
                status = response["messages"][-1].additional_kwargs.get('status', "")
                knowledgge_base_resp = self.extract_tool(
                    messages=response["messages"],
                    tool_name="knowledge_base_search",
                )
                text_to_sql_resp = self.extract_tool(
                    messages=response["messages"],
                    tool_name="text_to_sql",
                )

            self.logger.info(f"Received response from agent: {answer} for user query: {question}")

            sources = []
            if knowledgge_base_resp and knowledgge_base_resp.get("sources") is not None:
                try:
                    sources = json.loads(knowledgge_base_resp["sources"])
                except (TypeError, ValueError):
                    sources = knowledgge_base_resp.get("sources", [])

            if text_to_sql_resp and text_to_sql_resp.get("results") is not None:
                sources.append({"page_content": text_to_sql_resp.get("results")})

            return {
                "answer": answer,
                "sources": sources,
                "status": status,
                "knowledgge_base_resp": knowledgge_base_resp,
                "text_to_sql_resp": text_to_sql_resp,
            }

        except Exception as e:
            self.logger.error(f"Error while invoking agent: {e}")
            raise

    def extract_tool(self, messages, tool_name):
        for message in messages:
            if getattr(message, "type", None) == "tool" and getattr(message, "name", None) == tool_name:
                content = getattr(message, "content", "")
                try:
                    return json.loads(content)
                except (TypeError, ValueError):
                    return content
        return None



        

