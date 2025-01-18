from fastapi import APIRouter, HTTPException

from app.core.logger import setup_logging
from app.models.llm import LLMRequest, LLMResponse
from app.models.agent import AgentRequest, AgentResponse
from app.services.llm_service import route_llm_call
from app.services.llm_service import process_new_task


logger = setup_logging(__name__)

llm_router = APIRouter()

@llm_router.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the service is running.
    Returns a 200 status with a specific message if healthy, otherwise an error.
    """
    try:
        # Here you can add any logic to check the health of your service
        return {"message": "The answer is 42, always 42"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Service is not healthy")


@llm_router.post("/", response_model=LLMResponse)
async def llm_endpoint(request: LLMRequest):
    """
    Handle LLM requests and route to the appropriate model/provider.
    """
    try:
        result = route_llm_call(request.prompt)
        return LLMResponse(response=result["response"], redis_key=result["redis_key"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing LLM request: {str(e)}")
    

@llm_router.post("/process_new_task", response_model=LLMResponse)
async def process_new_task_endpoint(request: LLMRequest):
    """
    API endpoint to submit a new task for processing by the LLM worker.
    """
    try:
        # Publish the task to RabbitMQ and return the task ID
        task_id = process_new_task(request.prompt)
        logger.info(f"Task {task_id} submitted successfully.")
        
        return LLMResponse(
            response={"message": "Task submitted successfully."},
            redis_key=task_id
        )
    except Exception as e:
        logger.error(f"Error while submitting task: {e}")
        raise HTTPException(status_code=500, detail=f"Error submitting task: {str(e)}")

