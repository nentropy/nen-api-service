from pydantic import BaseModel
from typing import Optional, Dict


class LLMRequest(BaseModel):
    prompt: str

class LLMResponse(BaseModel):
    response: Dict  # For example, {"message": "Task submitted successfully."}
    redis_key: Optional[str]  # Task ID stored in Redis

class AgentRequest(BaseModel):
    task: str
    parameters: dict

class AgentResponse(BaseModel):
    result: dict
    redis_key: str
