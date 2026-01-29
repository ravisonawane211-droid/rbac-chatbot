from pydantic import Field , BaseModel 
from typing import List, Annotated, Dict, Any
from langchain.agents import AgentState
from langgraph.graph.message import add_messages



class AgentState(AgentState):
     messages: Annotated[list, add_messages]

     rag_response: Dict[str, Any]
