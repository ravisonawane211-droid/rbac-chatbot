from langchain.agents import create_agent
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.tools.knowledge_base import knowledge_base_search
from app.tools.text_to_sql import text_to_sql
from app.prompts.prompts import SMART_AGENT
from app.services.llm_service import LLMService
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain_core.prompts import PromptTemplate
from app.schemas.context import Context

llm_service = LLMService()

llm = llm_service._get_llm(llm_provider = llm_service.llm_provider,
                           llm_model = llm_service.llm_model, temperature=0.0)

@dynamic_prompt
def rag_prompt(request: ModelRequest) -> str:
    """Generate system prompt"""
    question = request.runtime.context.get("question", "")

    roles = request.runtime.context.get("roles",[])

    template = PromptTemplate.from_template(SMART_AGENT)

    prompt = template.format(question=question,roles = roles)

    return prompt

fin_solve_agent = create_agent(
    name="fin_solve_agent",
    model=llm,
    tools=[knowledge_base_search, text_to_sql],
    middleware=[rag_prompt],
    context_schema=Context,
    debug=True
)


if __name__ == "__main__":
    # The system prompt will be set dynamically based on context

    response = fin_solve_agent.invoke(input={"messages":[{"role": "user", "content": "Employee count and  Employee Onboarding & Benefits at FinSolve Technology"}]},
                                context={"question": "Employee count and  Employee Onboarding & Benefits at FinSolve Technology","roles": ["general"]})
    
    print(response["messages"][-1].text)

    # for chunk in knowledge_base_agent.stream(input={"messages":[{"role": "user", "content": "Employee count and  Employee Onboarding & Benefits at FinSolve Technology"}]},
    # context={"question": "Employee count and  Employee Onboarding & Benefits at FinSolve Technology"},
    # stream_mode="values"):
    # # Each chunk contains the full state at that point
    #     latest_message = chunk["messages"][-1]
    #     if latest_message.content:
    #         print(f"Agent: {latest_message.content}")
    #     elif latest_message.tool_calls:
    #         print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")