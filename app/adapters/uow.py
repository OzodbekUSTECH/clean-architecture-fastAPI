from app.abstractions.uow import IUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession

class SqlalchemyUnitOfWork(IUnitOfWork):
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
 
    async def commit(self) -> None:
        await self.session.commit()
 
    async def rollback(self) -> None:
        await self.session.rollback()


