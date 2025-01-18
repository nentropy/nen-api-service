import json
import time
import uuid

from core.logger import setup_logging
from core.portkey_client import get_portkey_client, pick_provider
from core.redis_client import store_short_term_memory
from core.redis_config import store_short_term_memory

from app.core.rabbitmq_client import publish_message

logger = setup_logging(__name__)

def route_llm_call(prompt: str):
    """
    Route the LLM call through the appropriate provider and log the output.
    """
    chosen_route = pick_provider(prompt)
    client = get_portkey_client(chosen_route)

    # Use appropriate model
    model_name = "claude-2" if "anthropic" in chosen_route else "gpt-4"

    # Make the LLM call
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model_name,
        max_tokens=128
    )

    # Store in Redis
    key = f"llm_response:{time.time()}"
    store_short_term_memory(key, completion)
    return {"response": completion, "redis_key": key}



def process_new_task(prompt: str) -> str:
    """
    Processes a new task by submitting it to RabbitMQ for the LLM worker.
    
    :param prompt: The user prompt to process.
    :return: The unique task ID.
    """
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    
    # Create the task payload
    task_payload = {
        "task_id": task_id,
        "prompt": prompt,
        "timestamp": time.time()
    }

    # Publish the task to RabbitMQ
    publish_message(queue_name="llm_queue", message=task_payload)
    logger.info(f"Task {task_id} published to LLM queue.")

    # Optionally store task status in Redis (set it to "PENDING")
    store_short_term_memory(key=f"task_status:{task_id}", data={"status": "PENDING"})

    return task_id

