from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from app.config.settings import settings
from app.controllers.parser import parse_router
from app.config.dishka import container_factory

app = FastAPI(
    title="Анализатор веб-сайтов",
    description="API для анализа веб-сайтов и определения их тематики"
)

container = container_factory()
setup_dishka(container, app)

app.include_router(
    parse_router,
    prefix="/api",
    tags=["Парсер"]
)

@app.get("/health", tags=["Система"])
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )