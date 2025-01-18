from fastapi import APIRouter, HTTPException
from app.services.manager_service import manage_task
from app.models.manager import ManagerRequest, ManagerResponse

router = APIRouter()

@router.post("/manage", response_model=ManagerResponse)
async def manage_task_endpoint(request: ManagerRequest):
    """
    Endpoint for managing and orchestrating tasks between multiple agents.
    """
    try:
        task_id = manage_task(request.workflow, request.parameters)
        return ManagerResponse(message="Manager task submitted successfully.", task_id=task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error managing task: {str(e)}")
