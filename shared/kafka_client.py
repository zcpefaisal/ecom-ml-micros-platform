from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json
import uuid
from datetime import datetime
from typing import Callable, List, Optional
import logging

logger = logging.getLogger(__name__)

class KafkaClient:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer: Optional[AIOKafkaProducer] = None

    async def start(self):
        """Start the kafka producer."""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers, 
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()
        logger.info("Kafka Producer started")

    async def stop(self):
        """Stop the kafka producer."""
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka Producer stopped")

    async def send_event(self, topic: str, event_type: str, data: dict):
        """Send an event to Kafka topics"""
        if not self.producer:
            await self.start()
        
        event = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "producer": "user-service", # will be set dynamically based on service
            "data": data
        }
    
        try:
            await self.producer.send_and_wait(topic, event)
            logger.info(f"Event send to topic {topic}: {event_type}")
        except Exception as e:
            logger.error(f"Failed to send event to topic {topic}: {e}")
            return False
        
class KafkaConsumer:
    def __inti__(self, bootstrap_servers: str, group_id: str):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer: Optional[AIOKafkaConsumer] = None
    
    async def consumer(self, topics: List[str], callable: Callable):
        """Consume messages from kafka topics"""
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        await self.consumer.start()
        logger.info(f"Kafka Consumer started for topics: {topics}")

        try:
            async for message in self.consumer:
                logger.info(f"Message received from topic {message.topic}: {message.value}")
                await callable(message.value)
        finally:
            await self.consumer.stop()
            logger.info("Kafka Consumer stopped")
