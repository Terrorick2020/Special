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
        """Генерация описания сайта с обработкой ошибок API"""
        try:
            content = await self._read_limited_content_async(content_file)
            prompt = f"Опиши чем занимается компания на русском языке (должно быть не более 3 предложений): {content}"
            logger.info(f"API Key: {self.api_key[:5]}...")  # Показываем только первые 5 символов для безопасности
                
            async with httpx.AsyncClient() as client:
                    logger.debug(f"Using API Key: {self.api_key}")
                    response = await client.post(
                        self.base_url,
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        json={
                            "model": self.model,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.7,
                            "max_tokens": 500
                        },
                        timeout=60
                    )
                    
                    response.raise_for_status()
                    response_data = response.json()
                    
                    if "error" in response_data:
                        logger.error(f"API Error: {response_data['error']}")
                        return "Не удалось сгенерировать описание"
                        
                    if "choices" not in response_data:
                        logger.error(f"Invalid API response: {response_data}")
                        return "Ошибка в структуре ответа API"
                        
                    return response_data["choices"][0]["message"]["content"]
                    
        except httpx.HTTPStatusError as e:
                logger.error(f"HTTP Error: {e.response.text}")
                return f"Ошибка API: {e.response.status_code}"
        except Exception as e:
                logger.error(f"Generation failed: {str(e)}")
                return "Ошибка генерации описания"

    async def _read_limited_content_async(self, file_path: Path, word_limit=300) -> str:
        """Асинхронное чтение файла с ограничением по количеству слов"""
        loop = asyncio.get_event_loop()
        
        content = await loop.run_in_executor(None, lambda: file_path.read_text(encoding="utf-8"))
        
        words = content.split()[word_limit:word_limit*2]
        return " ".join(words)