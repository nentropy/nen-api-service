from pydantic import BaseModel
from typing import Dict, List

from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

class BaseModelSchema(BaseModel):
    transaction_uuid: str
    timestamp: datetime
    user: str
    from_: str
    to: str

class ManagerRequest(BaseModelSchema):
    workflow: List[str]  # Example: ["schedule", "deploy"]
    parameters: Dict  # Example: { "schedule": { ... }, "deploy": { ... } }

class ManagerResponse(BaseModelSchema):
    message: str
    task_id: str
