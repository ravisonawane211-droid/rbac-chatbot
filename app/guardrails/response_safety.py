from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain_core.messages import AIMessage
from langchain.chat_models import init_chat_model
from langgraph.runtime import Runtime
from app.utils.logger import get_logger

logger = get_logger(__name__)

class SafetyGuardrailMiddleware(AgentMiddleware):

    def __init__(self):
        super().__init__()
        self.safety_model = init_chat_model("gpt-4.1-mini")
        logger.info(f"SafetyGuardrailMiddleware initialized with safety_model: {self.safety_model}")

    @hook_config(can_jump_to=["end"])
    def after_agent(self, state: AgentState, runtime: Runtime):
        logger.info("Running SafetyGuardrailMiddleware after agent response")

        if not state["messages"]:
            return None

        last_message = state["messages"][-1]

        if not isinstance(last_message, AIMessage):
            return None

        safety_prompt = f"""
        You are a safety classifier.

        Check if the response contains:
        - hacking instructions
        - illegal activity
        - malware creation
        - weapons or explosives guidance
        - harmful or dangerous advice

        Reply ONLY with SAFE or UNSAFE.

        Response:
        {last_message.content}
        """

        result = self.safety_model.invoke(
            [{"role": "user", "content": safety_prompt}]
        )

        decision = result.content.strip().upper()

        if decision.startswith("UNSAFE"):
            logger.warning(f"Unsafe response detected: {last_message.content}")
            return {
                    "messages": [{
                        "role": "assistant",
                        "content": "I cannot provide that response.Please rephrase your request. ",
                        "status": "ACCESS_DENIED"
                    }],
                    "jump_to": "end"
                }
        logger.info("Response is safe.")
        return None