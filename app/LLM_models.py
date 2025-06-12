from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState
from pydantic import BaseModel
from typing_extensions import Optional

class State(MessagesState):
    current_summary: str
    summary_prev: Optional[str]
    sys_message: SystemMessage

class Request(BaseModel):
    prompt: str
    user_id: int
    checksum: str
    summary_prev: str = ""