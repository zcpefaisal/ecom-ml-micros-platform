import os
from shared.kafka_client import KafkaClient

class EventHandler:
    def __init__(self):
        self.kafka_client = KafkaClient(
            bootstrap_servers=os.getenv("KAFKA_BROKER", "logalhost:9092")
        )

    async def send_user_created(self, user_data: dict):
        """Send user created event"""
        await self.kafka_client.start()
        await self.kafka_client.send_event(
            topic="users",
            event_type="user.created",
            data=user_data
        )

    async def send_user_updated(self, user_data: dict):
        """Send user updated event"""
        await self.kafka_client.send_event(
            topic="users",
            event_type="user.updated",
            data=user_data
        )