from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from app.config.settings import settings
from app.controllers.parser import parse_router
from app.config.dishka import container_factory

app = FastAPI(
    title="Website Analyzer",
    description="API для анализа веб-сайтов и определения их тематики"
)

setup_dishka(container_factory(), app)

app.include_router(
    parse_router,
    prefix="/api",
    tags=["Parser"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
