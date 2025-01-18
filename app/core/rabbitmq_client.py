import aio_pika
import pika
import json
from config import Config

config = Config()

def get_rabbitmq_connection():
    """
    Establish an asynchronous connection to RabbitMQ.
    """
    return aio_pika.connect_robust(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        login=config.RABBITMQ_USER,
        password=config.RABBITMQ_PASSWORD
    )

async def publish_message(queue_name: str, message: dict):
    """
    Asynchronously publish a message to a RabbitMQ queue.
    """
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()

        # Declare queue to ensure it exists
        await channel.declare_queue(queue_name, durable=True)

        # Publish message
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue_name
        )

def close_rabbitmq_connection(connection):
    """
    Close an existing RabbitMQ connection.
    """
    if connection:
        connection.close()