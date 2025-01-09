from modules.redis.redis_controller import RedisController
from modules.telegram.telegram_controller import TelegramController
import asyncio
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s", "%m-%d-%Y %H:%M:%S"
)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)


async def main():
    logger.info("App start")

    tg_controller = TelegramController()
    redis_controller = RedisController()

    await tg_controller.connect()
    await redis_controller.connect()
    await redis_controller.handle_redis_messages(tg_controller.send_message)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application stopped by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
