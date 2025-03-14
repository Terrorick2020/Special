# app/utils/helpers.py
import logging
import re
import time
import asyncio
from pathlib import Path
from typing import List, Optional, Callable
from functools import wraps
import httpx

def setup_logger(name: str = "app") -> logging.Logger:
    """Настройка логгера для приложения"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

def normalize_url(url: str, base_domain: str) -> str:
    """Нормализация URL-адресов"""
    if url.startswith("/"):
        return f"https://{base_domain}{url}"
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url

def is_valid_url(url: str) -> bool:
    """Проверка валидности URL"""
    url_pattern = re.compile(
        r"^(https?://)?"
        r"([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]{2,}"
        r"(:[0-9]{1,5})?"
        r"(/.*)?$"
    )
    return bool(url_pattern.match(url))

def clean_html_content(html: str) -> str:
    """Очистка HTML-контента"""
    from bs4 import BeautifulSoup
    try:
        soup = BeautifulSoup(html, "html.parser")
        
        for tag in ["script", "style", "nav", "footer", "header"]:
            for element in soup.find_all(tag):
                element.decompose()
        
        text = "\n".join(
            [p.get_text(strip=True) for p in soup.find_all(["p", "div", "section"])]
        )
        return "\n".join(line.strip() for line in text.splitlines() if line.strip())
    except Exception as e:
        return ""
        
def async_retry(max_retries: int = 3, delay: float = 1.0) -> Callable:
    """Декоратор для повторных асинхронных попыток"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except (httpx.RequestError, Exception) as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

def validate_domain(domain: str) -> bool:
    """Проверка валидности домена"""
    domain_pattern = re.compile(
        r"^([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    )
    return bool(domain_pattern.match(domain))

def chunk_text(text: str, max_words: int = 300) -> List[str]:
    """Разделение текста на части по количеству слов"""
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def file_operations(file_path: Path) -> None:
    """Декоратор для обработки файловых операций"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                return await func(*args, **kwargs)
            except (IOError, OSError) as e:
                logger = setup_logger()
                logger.error(f"File operation error: {str(e)}")
                raise
        return wrapper
    return decorator

def timing_decorator(func: Callable) -> Callable:
    """Декоратор для измерения времени выполнения"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start_time
        logger = setup_logger()
        logger.info(f"{func.__name__} executed in {duration:.2f} seconds")
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        logger = setup_logger()
        logger.info(f"{func.__name__} executed in {duration:.2f} seconds")
        return result

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper