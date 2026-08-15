from typing import Any
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
import logging

logger = logging.getLogger(__name__)


class SQLSafetyGuardrailMiddleware(AgentMiddleware):
    """
    LLM-based guardrail to detect SQL prompt injection or
    dangerous database modification requests.
    """

    def __init__(self):
        super().__init__()
        self.safety_model = init_chat_model("gpt-4.1-mini")
        logger.info("SQLSafetyGuardrailMiddleware initialized with safety_model: " + str(self.safety_model))

    @hook_config(can_jump_to=["end"])
    def before_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:

        if not state.get("messages"):
            return None

        last_message = state["messages"][-1]

        if not isinstance(last_message, HumanMessage):
            return None

        user_query = last_message.content

        safety_prompt = f"""
You are a database security classifier.

Determine if the user request attempts to modify,
delete, or destroy database data.

Mark UNSAFE if the request involves:
- DELETE data
- DROP tables
- TRUNCATE tables
- UPDATE records
- INSERT records
- ALTER schema
- removing or wiping database data

Allow only safe read operations.

Respond ONLY with:
SAFE
or
UNSAFE

User request:
{user_query}
"""

        result = self.safety_model.invoke(
            [{"role": "user", "content": safety_prompt}]
        )

        decision = result.content.strip().upper()

        if decision.startswith("UNSAFE"):

            logger.warning(f"Blocked SQL modification attempt: {user_query}")

            return {
                "messages": [{
                    "role": "assistant",
                    "content": "Database modification operations are not allowed. Please rephrase your request to only include data retrieval."
                }],
                "jump_to": "end"
            }
        logger.info("SQL request is safe.")

        return None