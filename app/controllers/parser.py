from fastapi import APIRouter, HTTPException
from pathlib import Path
from urllib.parse import unquote
from app.services.crawler import CrawlerService
from app.services.ai_processor import AIProcessor
from app.utils.helpers import setup_logger, is_valid_url
import traceback

logger = setup_logger(__name__)

router = APIRouter()

# Инициализация сервисов
crawler = CrawlerService()
ai = AIProcessor()

@router.get("/parse/{url:path}")
async def parse_website(url: str):
    try:
        # Декодирование URL
        decoded_url = unquote(url)
        
        logger.info(f"Processing URL: {decoded_url}")
        
        # Проверка валидности URL
        if not is_valid_url(decoded_url):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Обработка запроса
        result = await crawler.process_site(decoded_url)
        
        # Проверка наличия контента
        content_file = Path(result["content_file"])
        if not content_file.exists() or content_file.stat().st_size == 0:
            raise HTTPException(status_code=404, detail="No content found")
            
        # Генерация описания
        description = await ai.generate_description(content_file)
        
        return {
            "domain": result["domain"],
            "subdomains_count": len(result["subdomains"]),
            "pages_found": result["pages_found"],
            "description": description,
            "content_file": str(content_file)
        }
    except HTTPException as he:
        raise
    except Exception as e:
        logger.error(f"Critical error processing {url}: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")