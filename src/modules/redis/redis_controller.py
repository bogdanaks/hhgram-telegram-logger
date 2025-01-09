import asyncio
import logging
from typing import Callable
import redis.asyncio as redis
from configs.config import BaseConfig

logger = logging.getLogger(__name__)


class RedisController:
    def __init__(self) -> None:
        self.redis = None

    async def connect(self):
        try:
            self.redis = await redis.from_url(
                f"redis://{BaseConfig.REDIS_HOST}:{BaseConfig.REDIS_PORT}",
                decode_responses=True,
            )
            logger.info(
                f"Connected to Redis at {BaseConfig.REDIS_HOST}:{BaseConfig.REDIS_PORT}"
            )
        except asyncio.TimeoutError as e:
            logger.error(f"Timeout while connecting to Redis: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def handle_redis_messages(self, callback: Callable):
        if self.redis is None:
            await self.connect()

        pubsub = self.redis.pubsub()
        await pubsub.subscribe(BaseConfig.REDIS_CHANNEL)
        logger.info(f"Subscription to channel {BaseConfig.REDIS_CHANNEL} established.")

        try:
            async for message in pubsub.listen():
                if message["type"] == "subscribe":
                    continue

                logger.info(f"Received message from Redis: {message}")
                if message["type"] == "message":
                    content = message["data"]
                    await callback(content)
        except Exception as e:
            logger.error(f"Error while listening to Redis channel: {e}")
            await self.handle_redis_messages(callback)
