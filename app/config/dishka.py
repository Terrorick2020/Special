from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config.settings import settings
from app.services.crawler import CrawlerService
from app.services.ai_processor import AIProcessor
from app.database.repository import ResultRepository

class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self):
        return create_async_engine(
            f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
            f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
            f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
            echo=True
        )

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine) -> async_sessionmaker:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_factory: async_sessionmaker) -> AsyncSession:
         return session_factory()

class ServicesProvider(Provider):
    crawler_service = provide(CrawlerService, scope=Scope.REQUEST)
    ai_processor = provide(AIProcessor, scope=Scope.REQUEST)
    result_repository = provide(ResultRepository, scope=Scope.REQUEST)

def container_factory():
    from dishka import make_async_container
    return make_async_container(
        DatabaseProvider(),
        ServicesProvider(),
    )