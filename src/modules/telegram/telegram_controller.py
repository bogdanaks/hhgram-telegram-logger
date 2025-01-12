import json
import logging
from datetime import datetime
from telethon import TelegramClient

from configs.config import BaseConfig

logger = logging.getLogger(__name__)


class TelegramController:
    def __init__(
        self,
    ) -> None:
        self.client = TelegramClient(
            session=BaseConfig.TG_SESSION,
            api_id=BaseConfig.TG_APP_ID,
            api_hash=BaseConfig.TG_APP_HASH,
        )

    async def connect(self):
        logger.info("Telegram client connecting...")

        await self.client.start(phone=BaseConfig.TG_PHONE)  # type: ignore

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(phone=BaseConfig.TG_PHONE)
            code = input("Enter code: ")
            await self.client.sign_in(code)

        logger.info("Telegram client connected!")

    async def send_message(self, content: str):
        try:
            data = json.loads(content)
            level: str = data["level"]
            name: str = data["name"]
            message: str = data["message"]
            time: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Sending message to Telegram: {message}")
            emoji_type = self._get_emoji_by_type(level.lower())
            formatted_message = (
                f"**{emoji_type} {level.upper()}** | {time}\n"
                # f"**Logger:** {name}\n\n"
                f"**Message:** {message}\n"
            )

            await self.client.send_message(
                BaseConfig.TG_LOGGER_ID,
                formatted_message,
                link_preview=False,
                background=True,
            )
        except Exception as e:
            logger.error(f"Error sending message to Telegram: {e}")

    def _get_emoji_by_type(self, type: str):
        if type == "info":
            return "ℹ️"
        elif type == "warning":
            return "⚠️"
        elif type == "error":
            return "❌"
        elif type == "critical":
            return "🚨"
        else:
            return "❓"
