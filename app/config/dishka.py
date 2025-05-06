from typing import Protocol
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.config.settings import settings
from app.services.crawler import CrawlerService
from app.services.ai_processor import AIProcessor
from app.database.repository import ResultRepository

# Определим протоколы для сервисов
class CrawlerProtocol(Protocol):
    async def process_site(self, url: str) -> dict:
        ...

class AIProcessorProtocol(Protocol):
    async def generate_description(self, content_file) -> str:
        ...

class RepositoryProtocol(Protocol):
    async def create_result(self, result_data: dict): 
        ...
    async def get_results_by_domain(self, domain: str):
        ...

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
        async with session_factory() as session:
            yield session
           
    @provide
    def provide_crawler(self) -> CrawlerProtocol:
        return CrawlerService()

    @provide
    def provide_ai_processor(self) -> AIProcessorProtocol:
        return AIProcessor()

    @provide
    def provide_repository(self, session: AsyncSession) -> RepositoryProtocol:
        return ResultRepository(session)

def container_factory():
    from dishka import make_async_container
    return make_async_container(
        DatabaseProvider(),
        RequestProvider(),
    )