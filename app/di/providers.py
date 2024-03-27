from app.di.scopes import singleton_factory
from app.di.stub import Stub
from typing import Annotated, AsyncIterable
from fastapi import Depends
from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession



@singleton_factory()
def create_engine() -> AsyncEngine:
    return create_async_engine(settings.DATABASE_URL, echo=settings.ECHO)


@singleton_factory()
def create_session_maker(
    engine: Annotated[AsyncEngine, Depends(Stub(AsyncEngine))],
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def new_session(
    session_maker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(Stub(async_sessionmaker[AsyncSession])),
    ],
) -> AsyncIterable[AsyncSession]:
    async with session_maker() as session:
        yield session

from app.abstractions.blogs import IBlogsRepository
from app.abstractions.uow import IUnitOfWork
from app.adapters.blogs import SqlalchemyBlogsrRepository
from app.adapters.uow import SqlalchemyUnitOfWork
from app.services.blogs import BlogsService

def new_unit_of_work(
    session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> IUnitOfWork:
    return SqlalchemyUnitOfWork(session)

def new_blog_repository(
    session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> IBlogsRepository:
    return SqlalchemyBlogsrRepository(session)

 
def new_blog_service(
    uow: Annotated[IUnitOfWork, Depends()],
    user_repository: Annotated[IBlogsRepository, Depends()],
) -> BlogsService:
    return BlogsService(uow, user_repository)