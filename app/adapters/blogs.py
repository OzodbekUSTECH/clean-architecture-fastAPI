from app.models import Blog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from app.abstractions.blogs import IBlogsRepository



class SqlalchemyBlogsRepository(IBlogsRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
 
    async def save_blog(self, data: dict) -> None:
        query = insert(Blog).values(**data)
 
        await self.session.execute(query)
 
    async def get_blog(self, id: int) -> Blog | None:
        query = select(Blog).where(Blog.id == id)
 
        result = await self.session.execute(query)
        result = result.scalar_one_or_none()
 
        return result
 