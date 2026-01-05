import asyncio
import os
import logging
from shared.kafka_client import KafkaConsumer

logger = logging.getLogger(__name__)

async def handle_user_created(event: dict):
    """Handle user created event"""
    logger.info(f"User created: {event['data']}")


async def handle_order_events(event: dict):
    """Handle order-related events"""
    logger.info(f"Order event: {event['event_type']}")

async def start_kafka_consumer():
    """Start kafka consumer for order service"""
    consumer = KafkaConsumer(
        bootstrap_servers=os.getenv("KAFKA_BROKER", "localhost:9092"),
        group_id="order-service-group"
    )

    # Map event types to handlers
    event_handlers = {
        "user.created": handle_user_created,
        "user.updated": handle_user_created,
        "order.created": handle_order_events
    }

    async def message_handler(message: dict):
        event_type = message.get("event_type")
        handler = event_handlers.get(event_type)
        if handler:
            await handler(message)
        else:
            logger.warning(f"No handler for event type: {event_type}")

    await consumer.consumer(["users", "orders"], message_handler)