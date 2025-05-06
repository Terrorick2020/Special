from fastapi import APIRouter, HTTPException, status, Depends
from pathlib import Path
from urllib.parse import unquote
from typing import Any

from app.services.crawler import CrawlerService
from app.services.ai_processor import AIProcessor
from app.database.repository import ResultRepository
from app.database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helpers import setup_logger, is_valid_url
from app.schemas.results import ResultResponse
import traceback

logger = setup_logger(__name__)

router = APIRouter()

# Функции для получения зависимостей
def get_crawler() -> CrawlerService:
    return CrawlerService()

def get_ai_processor() -> AIProcessor:
    return AIProcessor()

def get_repository(session: AsyncSession = Depends(get_session)) -> ResultRepository:
    return ResultRepository(session)

@router.get(
    "/parse/{url:path}",
    response_model=ResultResponse,
    status_code=status.HTTP_200_OK
)
async def parse_website(
    url: str,
    crawler: Any = Depends(get_crawler),
    ai: Any = Depends(get_ai_processor),
    repository: Any = Depends(get_repository),
):
    try:
        decoded_url = unquote(url)
        logger.info(f"Обработка: {decoded_url}")

        if not is_valid_url(decoded_url):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Некорректный URL"
            )

        result = await crawler.process_site(decoded_url)
        content_file = Path(result["content_file"])

        if not content_file.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Файл не найден"
            )
            
        if content_file.stat().st_size < 100:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Недостаточно данных"
            )

        description = await ai.generate_description(content_file)
        
        if "ошибка" in description.lower():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=description
            )

        result_data = {
            "domain": result["domain"],
            "subdomains_count": len(result["subdomains"]),
            "pages_found": result["pages_found"],
            "description": description,
            "content_file_path": str(content_file)
        }

        db_result = await repository.create_result(result_data)
        return db_result

    except HTTPException as he:
        logger.error(f"HTTP ошибка: {he.detail}")
        raise
    except Exception as e:
        logger.critical(f"Критическая ошибка: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

parse_router = router