from fastapi import FastAPI, Depends
from dishka.integrations.fastapi import setup_dishka, DishkaRoute

from app.config.settings import settings
from app.controllers.parser import parse_router
from app.config.dishka import container_factory

app = FastAPI(
    title="Анализатор веб-сайтов",
    description="API для анализа веб-сайтов и определения их тематики"
)

# Настраиваем dishka
setup_dishka(container_factory(), app)

app.include_router(
    parse_router,
    prefix="/api",
    tags=["Парсер"]
)

# Добавим эндпоинт для healthcheck
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