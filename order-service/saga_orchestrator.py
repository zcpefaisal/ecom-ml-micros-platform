from enum import Enum
from typing import List, Dict, Any, Callable
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SagaStatus(Enum):
    PENDING = "pending"
    COMPENSATING = "compensating"
    COMPLETED = "completed"
    FAILED = "failed"

class SagaStep:
    def __init__(self, name: str, execute: Callable, compensate: Callable):
        self.name = name
        self.execute = execute
        self.compensate = compensate
        self.status = SagaStatus.PENDING

class SagaOrchestrator:
    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.steps: List[SagaStep] = []
        self.status = SagaStatus.PENDING
        self.created_at = datetime.utcnow()

    def add_step(self, step: SagaStep):
        self.steps.append(step)

    async def execute(self):
        """Execute all saga steps"""
        completed_steps = []

        try:
            for step in self.steps:
                logger.info(f"Executing saga step: {step.name}")
                await step.execute()
                step.status = SagaStatus.COMPLETED
                completed_steps.append(step)
                
            self.status = SagaStatus.COMPLETED
            logger.info(f"Saga {self.saga_id} completed successfully")
            return True
        
        except Exception as e:
            logger.error(f"Saga {self.saga_id} failed: {e}")
            self.status = SagaStatus.FAILED
            
            # Execute compensation in reverse order
            await self.compensate(completed_steps)
            return False
        
    async def compensate(self, completed_steps: List[SagaStep]):
        """Compensate completed steps"""
        logger.info(f"Starting compensation for saga {self.saga_id}")
        self.status = SagaStatus.COMPENSATING
        
        for step in reversed(completed_steps):
            try:
                logger.info(f"Compensating step: {step.name}")
                await step.compensate()
            except Exception as e:
                logger.error(f"Failed to compensate step {step.name}: {e}")