import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    TG_APP_ID: int = int(os.environ.get("TG_APP_ID", 0))
    TG_APP_HASH: str = os.environ.get("TG_APP_HASH", "")
    TG_SESSION: str = os.environ.get("TG_SESSION", "")
    TG_PHONE: str = os.environ.get("TG_PHONE", "")
    TG_LOGGER_ID: int = int(os.environ.get("TG_LOGGER_ID", 0))

    REDIS_HOST: str = os.environ.get("REDIS_HOST", "")
    REDIS_PORT: str = os.environ.get("REDIS_PORT", "")
    REDIS_CHANNEL: str = os.environ.get("REDIS_CHANNEL", "")
