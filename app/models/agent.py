from pydantic import BaseModel

class AgentRequest(BaseModel):
    task: str
    parameters: dict

class AgentResponse(BaseModel):
    result: dict
