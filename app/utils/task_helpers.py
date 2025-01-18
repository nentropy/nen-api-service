from core.rabbitmq_client import publish_message
import uuid
import time
from ..core.logger import setup_logging

logger = setup_logging(__name__)

def trigger_agent_task(agent: str, parameters: dict) -> dict:
    """
    Trigger a task for an agent and wait for the result.

    :param agent: The name of the agent (e.g., "executive", "gcp_config").
    :param parameters: Parameters for the agent task.
    :return: The result from the agent.
    """
    task_id = str(uuid.uuid4())
    task_message = {
        "task_id": task_id,
        "parameters": parameters,
        "timestamp": time.time()
    }

    logger.info(f"Triggering task for agent: {agent} with task_id: {task_id}")

    # Publish the task to the agent-specific RabbitMQ queue
    queue_name = f"{agent}_queue"
    publish_message(queue_name=queue_name, message=task_message)

    logger.info(f"Task published to queue: {queue_name} with task_id: {task_id}")

    # Simulate waiting for a result (in a real system, this would query Redis or another store)
    result = {"status": "COMPLETED", "agent": agent, "task_id": task_id, "result": f"Result for {agent}"}
    logger.info(f"Task completed for agent: {agent} with task_id: {task_id}, result: {result}")
    return result

def aggregate_results(results: dict) -> dict:
    """
    Aggregate results from multiple agents into a single response.

    :param results: Dictionary of results from different agents.
    :return: Aggregated result.
    """
    logger.info("Aggregating results from multiple agents.")
    # Example: Combine all results into one dictionary
    aggregated = {"agents": results, "summary": "All tasks completed successfully."}
    logger.info(f"Aggregated result: {aggregated}")
    return aggregated
