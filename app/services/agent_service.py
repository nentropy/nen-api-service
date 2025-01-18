import json
import time
import uuid

from core.logger import setup_logging
from core.rabbitmq_client import process_task, publish_message
from core.redis_config import store_short_term_memory

logger = setup_logging(__name__)

def query_gcp_agent(task: str, parameters: dict):
    """
    Handle GCP agent requests.
    """
    return process_task(task, parameters)

def trigger_agent_action(task: str, parameters: dict) -> str:
    """
    Submit an agent action task to RabbitMQ for processing.

    :param task: The name of the agent task to perform (e.g., "query_data").
    :param parameters: Parameters required for the task (e.g., query details).
    :return: The unique task ID.
    """
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    
    # Create the task payload
    task_payload = {
        "task_id": task_id,
        "task": task,
        "parameters": parameters,
        "timestamp": time.time()
    }

    # Publish the task to RabbitMQ (to the agent queue)
    publish_message(queue_name="agent_queue", message=task_payload)
    logger.info(f"Agent task {task_id} published to RabbitMQ.")

    # Optionally store task status in Redis
    store_short_term_memory(
        key=f"agent_task_status:{task_id}",
        data={"status": "PENDING"}
    )

    return task_id