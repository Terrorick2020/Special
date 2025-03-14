import httpx
from pathlib import Path
from app.config.settings import settings
import asyncio
from app.utils.helpers import (
    setup_logger,
    async_retry,
    timing_decorator,
)

logger = setup_logger(__name__)

class AIProcessor:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.model = settings.DEEPSEEK_MODEL
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    @async_retry(max_retries=settings.MAX_RETRIES, delay=settings.RETRY_DELAY)
    @timing_decorator
    async def generate_description(self, content_file: Path) -> str:
        """Генерация описания сайта (асинхронная версия)"""
        content = await self._read_limited_content_async(content_file)
        prompt = f"Опиши чем занимается компания: {content}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "messages": [{"role": "user", "content": prompt}]},
                timeout=30
            )
        
        return response.json()["choices"][0]["message"]["content"]

    async def _read_limited_content_async(self, file_path: Path, word_limit=300) -> str:
        """Асинхронное чтение файла с ограничением по количеству слов"""
        loop = asyncio.get_event_loop()
        
        content = await loop.run_in_executor(None, lambda: file_path.read_text(encoding="utf-8"))
        
        words = content.split()[word_limit:word_limit*2]
        return " ".join(words)