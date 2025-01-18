from app.core.rabbitmq_client import publish_message
import uuid

def manage_task(workflow: list, parameters: dict) -> str:
    """
    Submit a manager task to RabbitMQ for processing.

    :param workflow: List of agent tasks to orchestrate (e.g., ["schedule", "deploy"]).
    :param parameters: Parameters for each agent task.
    :return: The unique task ID for the manager task.
    """
    task_id = str(uuid.uuid4())
    message = {
        "task_id": task_id,
        "workflow": workflow,
        "parameters": parameters
    }
    
    # Publish the task to the manager queue
    publish_message(queue_name="manager_queue", message=message)
    return task_id