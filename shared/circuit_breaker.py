from circuitbreaker import CircuitBreaker
import logging
import httpx
import asyncio
from typing import Any, Dict, Optional
from functools import wraps

logger = logging.getLogger(__name__)

class ServiceUnavailableException(Exception):
    """Custom exception to indicate that a service is unavailable."""
    pass

class CircuitBreaker:

    @staticmethod
    @circuit(
        failure_threshold=5,
        recovery_timeout=30,
        excepted_exceptions=httpx.RequestError
    )
    async def call_service(
        self,
        method: str,
        url: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Any:
        """Make an HTTP call to another service with circuit breaker protection."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers)
                elif method.upper() == "POST":
                    response = await client.post(url, json=data, headers=headers)
                elif method.upper() == "PUT":
                    response = await client.put(url, json=data, headers=headers)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
            
            except httpx.RequestError as e:
                logger.error(f"Request error when calling {url}: {e}")
                raise

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error when calling {url}: {e}")
                raise

    async def call_with_fallback(
        self,
        method: str,
        url: str,
        fallback_value: Any,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Any:
        """Call the service with a fallback in case of failure."""
        try:
            return await self.call_service(method, url, data, headers)
        except Exception as e:
            logger.warning(f"Service call failed, executing fallback: {e}")
            if fallback_value:
                return fallback_value
            