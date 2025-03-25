from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.config.settings import settings
from app.services.crawler import CrawlerService
from app.services.ai_processor import AIProcessor
from app.database.repository import ResultRepository

class DatabaseProvider(Provider):
    scope = Scope.APP  
    
    @provide
    def provide_engine(self) -> create_async_engine:
        return create_async_engine(settings.DATABASE_URL, echo=True)

    @provide
    def provide_session_factory(self, engine: create_async_engine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

class RequestProvider(Provider):
    scope = Scope.REQUEST
    
    @provide
    async def provide_session(self, session_factory: async_sessionmaker[AsyncSession]) -> AsyncSession:
        return session_factory()
           

    @provide
    def provide_crawler(self) -> CrawlerService:
        return CrawlerService()

    @provide
    def provide_ai_processor(self) -> AIProcessor:
        return AIProcessor()

    @provide
    def provide_repository(self, session: AsyncSession) -> ResultRepository:
        return ResultRepository(session)

def container_factory():
    from dishka import make_async_container
    return make_async_container(
        DatabaseProvider(),
        RequestProvider(),
    )