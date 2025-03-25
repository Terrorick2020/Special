from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Result

class ResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_result(self, result_data: dict) -> Result:
        result = Result(**result_data)
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def get_results_by_domain(self, domain: str):
        from app.database.models import Result
        from sqlalchemy import select
        result = await self.session.execute(
            select(Result).where(Result.domain == domain))
        return result.scalars().all()