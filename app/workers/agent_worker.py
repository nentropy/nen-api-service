import json

from core.logger import setup_logging
from core.rabbitmq_client import get_rabbitmq_connection
from core.redis_config import store_short_term_memory

logger = setup_logging(__name__)

def process_agent_task(ch, method, properties, body):
    """
    Process an agent task received from RabbitMQ.
    """
    try:
        # Decode the task message
        task = json.loads(body)
        task_id = task.get("task_id")
        action = task.get("task")
        parameters = task.get("parameters")
        
        if not task_id or not action or parameters is None:
            raise ValueError("Task message is missing required fields")

        logger.debug(f"Decoded task: {task}")
        logger.info(f"Processing agent task: {task_id} with action: {action}")

        # Simulate agent task processing (replace with actual GCP agent logic)
        result = perform_agent_action(action, parameters)  # Simulated action

        # Store the result in Redis
        store_short_term_memory(
            key=f"agent_task_result:{task_id}",
            data={"result": result, "status": "COMPLETED"}
        )
        logger.info(f"Task {task_id} completed. Result stored in Redis.")

        # Acknowledge the task in RabbitMQ
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode task message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except ValueError as e:
        logger.error(f"Invalid task data: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        logger.error(f"Unexpected error processing agent task: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def perform_agent_action(action: str, parameters: dict) -> dict:
    """
    Simulate the execution of an agent action. Replace this with actual agent logic.

    :param action: The name of the action to perform (e.g., "query_data").
    :param parameters: Parameters required for the action.
    :return: The result of the action.
    """
    if action == "query_data":
        # Simulate querying data (replace with actual GCP API call)
        return {
            "query": parameters.get("query"),
            "rows_returned": 100,
            "status": "success"
        }
    elif action == "analyze_text":
        # Simulate text analysis
        return {
            "text": parameters.get("text"),
            "sentiment": "positive",
            "confidence": 0.95
        }
    else:
        raise ValueError(f"Unknown action: {action}")

def start_agent_worker():
    """
    Start a worker to consume tasks from the agent queue.
    """
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declare the agent queue
    channel.queue_declare(queue="agent_queue", durable=True)

    # Set up consumer
    channel.basic_qos(prefetch_count=1)  # Process one task at a time
    channel.basic_consume(queue="agent_queue", on_message_callback=process_agent_task)

    logger.info("Agent Worker started. Waiting for tasks...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Agent Worker stopped by user.")
        channel.stop_consuming()
    finally:
        connection.close()
