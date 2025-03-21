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
        decoded_url = unquote(url)
        logger.info(f"Processing: {decoded_url}")

        if not is_valid_url(decoded_url):
            raise HTTPException(status_code=400, detail="Некорректный URL")

        result = await crawler.process_site(decoded_url)
        content_file = Path(result["content_file"])

        if not content_file.exists():
            raise HTTPException(status_code=404, detail="Файл не найден")
            
        if content_file.stat().st_size < 100:
            raise HTTPException(status_code=422, detail="Недостаточно данных")

        description = await ai.generate_description(content_file)
        
        if "ошибка" in description.lower():
            raise HTTPException(status_code=500, detail=description)

        return {
            "domain": result["domain"],
            "subdomains_count": len(result["subdomains"]),
            "pages_found": result["pages_found"],
            "description": description,
            "content_file": str(content_file)
        }

    except HTTPException as he:
        logger.error(f"HTTP Error: {he.detail}")
        raise
    except Exception as e:
        logger.critical(f"Critical error: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )