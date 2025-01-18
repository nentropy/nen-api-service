import json
from app.core.rabbitmq_client import get_rabbitmq_connection
from app.core.redis_client import store_short_term_memory
from app.core.logger import setup_logging
from app.utils.task_helpers import trigger_agent_task, aggregate_results

logger = setup_logging(__name__)

def process_manager_task(ch, method, properties, body):
    """
    Process a manager task received from RabbitMQ. 
    Orchestrates tasks between multiple agents.
    """
    try:
        # Decode the task message
        task = json.loads(body)
        task_id = task["task_id"]
        workflow = task["workflow"]
        parameters = task["parameters"]
        
        logger.info(f"Processing manager task: {task_id} with workflow: {workflow}")

        # Trigger agent tasks and wait for their completion
        results = {}
        for agent in workflow:
            agent_result = trigger_agent_task(agent, parameters.get(agent, {}))
            results[agent] = agent_result

        # Aggregate results (if needed)
        aggregated_result = aggregate_results(results)

        # Store the aggregated result in Redis
        store_short_term_memory(
            key=f"manager_task_result:{task_id}",
            data={"result": aggregated_result, "status": "COMPLETED"}
        )
        logger.info(f"Manager task {task_id} completed successfully.")

        # Acknowledge the task in RabbitMQ
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Error processing manager task: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_manager_worker():
    """
    Start a worker to consume tasks from the manager queue.
    """
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declare the manager queue
    channel.queue_declare(queue="manager_queue", durable=True)

    # Set up consumer
    channel.basic_qos(prefetch_count=1)  # Process one task at a time
    channel.basic_consume(queue="manager_queue", on_message_callback=process_manager_task)

    logger.info("Manager Worker started. Waiting for tasks...")
    channel.start_consuming()
