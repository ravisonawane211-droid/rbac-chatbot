from typing import Any
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime
from langchain.messages import HumanMessage
import logging

logger = logging.getLogger(__name__)


class PromptInjectionMiddleware(AgentMiddleware):

    def __init__(self):
        super().__init__()

        self.injection_patterns = [
            "ignore previous instructions",
            "ignore all previous instructions",
            "reveal system prompt",
            "show system prompt",
            "act as system",
            "act as developer",
            "jailbreak",
            "bypass restrictions",
            "override safety"
        ]
        logger.info("PromptInjectionMiddleware initialized with patterns: " + ", ".join(self.injection_patterns))

    @hook_config(can_jump_to=["end"])
    def before_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        logger.info("Running PromptInjectionMiddleware before agent execution")

        if not state.get("messages"):
            logger.warning("No messages found in state during prompt injection check")
            return None

        last_message = state["messages"][-1]

        if not isinstance(last_message, HumanMessage):
            logger.warning("Last message is not a HumanMessage during prompt injection check")
            return None

        query = last_message.content.lower()

        for pattern in self.injection_patterns:
            if pattern in query:

                logger.warning(f"Prompt injection detected: {query}")

                return {
                    "messages": [{
                        "role": "assistant",
                        "content": "Your request contains instructions that attempt to manipulate the system and cannot be processed.",
                         "status": "ACCESS_DENIED"
                    }],
                    "jump_to": "end"
                }
        logger.info("No prompt injection detected in user input")
        return None