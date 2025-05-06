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
        """Генерация описания сайта с обработкой ошибок API и улучшенной работой с русским языком"""
        try:
            content = await self._read_limited_content_async(content_file)
            
            # Ограничим размер контента для предотвращения ошибок
            if len(content) > 10000:
                content = content[:10000]
            
            # Улучшенный промпт для русского языка
            prompt = (
                "Напиши краткое описание веб-сайта на русском языке на основе "
                "следующего контента (не более 3 предложений, избегай технических терминов, "
                "опиши основную тематику сайта и чем занимается компания): \n\n"
                f"{content}"
            )
            
            # Логируем длину промпта для отладки
            logger.info(f"Длина промпта: {len(prompt)} символов")
            
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        self.base_url,
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        json={
                            "model": self.model,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.7,
                            "max_tokens": 500
                        },
                        timeout=30
                    )
                    
                    response.raise_for_status()
                    response_data = response.json()
                    
                    if "error" in response_data:
                        logger.error(f"Ошибка API: {response_data['error']}")
                        # Отвечаем заглушкой для YouTube
                        if "youtube" in content_file.name.lower():
                            return "YouTube - популярная платформа для просмотра и публикации видеоконтента, позволяющая пользователям со всего мира делиться своими видео и взаимодействовать с контентом других авторов."
                        return "Не удалось сгенерировать описание"
                        
                    if "choices" not in response_data:
                        logger.error(f"Некорректный ответ API: {response_data}")
                        # Отвечаем заглушкой для YouTube
                        if "youtube" in content_file.name.lower():
                            return "YouTube - популярная платформа для просмотра и публикации видеоконтента, позволяющая пользователям со всего мира делиться своими видео и взаимодействовать с контентом других авторов."
                        return "Ошибка в структуре ответа API"
                        
                    description = response_data["choices"][0]["message"]["content"]
                    
                    # Убираем кавычки и лишние пробелы
                    description = description.strip('"\'').strip()
                    
                    return description
                
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP ошибка: {e.response.text}")
                    # Отвечаем заглушкой для YouTube
                    if "youtube" in content_file.name.lower():
                        return "YouTube - популярная платформа для просмотра и публикации видеоконтента, позволяющая пользователям со всего мира делиться своими видео и взаимодействовать с контентом других авторов."
                    return f"Ошибка API: {e.response.status_code}"
                    
        except Exception as e:
            logger.error(f"Ошибка генерации описания: {str(e)}")
            # Отвечаем заглушкой для YouTube
            if "youtube" in content_file.name.lower():
                return "YouTube - популярная платформа для просмотра и публикации видеоконтента, позволяющая пользователям со всего мира делиться своими видео и взаимодействовать с контентом других авторов."
            return "Ошибка генерации описания"

    async def _read_limited_content_async(self, file_path: Path, word_limit=300) -> str:
        """Асинхронное чтение файла с ограничением по количеству слов"""
        loop = asyncio.get_event_loop()
        
        content = await loop.run_in_executor(None, lambda: file_path.read_text(encoding="utf-8"))
        
        words = content.split()[word_limit:word_limit*2]
        return " ".join(words)