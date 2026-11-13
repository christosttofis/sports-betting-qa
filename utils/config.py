import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str
    user_id: str
    headless: bool
    timeout: int

    @property
    def app_url(self) -> str:
        return f"{self.base_url}/?user-id={self.user_id}"

    @property
    def api_url(self) -> str:
        return f"{self.base_url}/api"


def load_settings() -> Settings:
    user_id = os.getenv("USER_ID", "").strip()
    if not user_id or user_id.startswith("<"):
        raise RuntimeError("USER_ID is not set. Copy .env.example to .env and fill it in.")

    return Settings(
        base_url=os.getenv("BASE_URL", "https://qae-assignment-tau.vercel.app").rstrip("/"),
        user_id=user_id,
        headless=os.getenv("HEADLESS", "false").lower() == "true",
        timeout=int(os.getenv("TIMEOUT", "10")),
    )
