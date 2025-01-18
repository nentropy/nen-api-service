import json

from core.logger import setup_logging
from core.rabbitmq_client import get_rabbitmq_connection
from core.redis_config import store_short_term_memory

logger = setup_logging(__name__)

def process_llm_task(ch, method, properties, body):
    """
    Process an LLM task received from RabbitMQ.
    """
    try:
        # Decode the task message
        task = json.loads(body)
        task_id = task["task_id"]
        prompt = task["prompt"]
        
        logger.info(f"Processing LLM task: {task_id}")

        # Simulate processing the LLM task (replace this with actual LLM logic)
        llm_result = f"Processed prompt: {prompt}"  # Simulated response

        # Store the result in Redis
        store_short_term_memory(key=f"task_result:{task_id}", data={"result": llm_result, "status": "COMPLETED"})

        logger.info(f"Task {task_id} completed successfully. Result stored in Redis.")

        # Acknowledge the task in RabbitMQ
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Error while processing task: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_llm_worker():
    """
    Start a worker to consume tasks from the LLM queue.
    """
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declare the LLM queue
    channel.queue_declare(queue="llm_queue", durable=True)

    # Set up consumer
    channel.basic_qos(prefetch_count=1)  # Process one task at a time
    channel.basic_consume(queue="llm_queue", on_message_callback=process_llm_task)

    logger.info("LLM Worker started. Waiting for tasks...")
    channel.start_consuming()
