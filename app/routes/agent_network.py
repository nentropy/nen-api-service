from fastapi import APIRouter, HTTPException
from app.services.agent_service import query_gcp_agent
from app.models.agent import AgentRequest, AgentResponse

router = APIRouter()

@router.post("/gcp", response_model=AgentResponse)
async def gcp_agent_endpoint(request: AgentRequest):
    """
    Endpoint for querying GCP agent.
    """
    try:
        result = query_gcp_agent(request.task, request.parameters)
        return AgentResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GCP agent error: {str(e)}")

@router.post("/trigger_action", response_model=AgentResponse)
async def trigger_action_endpoint(request: AgentRequest):
    """
    API endpoint to trigger an agent action.
    """
    try:
        # Submit the agent action to RabbitMQ
        task_id = trigger_agent_action(request.task, request.parameters)
        logger.info(f"Agent action triggered successfully. Task ID: {task_id}")

        return AgentResponse(
            result={
                "message": "Agent action triggered successfully.",
                "task_id": task_id
            }
        )
    except Exception as e:
        logger.error(f"Error while triggering agent action: {e}")
        raise HTTPException(status_code=500, detail=f"Error triggering agent action: {str(e)}")
