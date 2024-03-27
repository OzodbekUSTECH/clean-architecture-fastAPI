from app.di.scopes import singleton_factory
from app.di.stub import Stub
from typing import Annotated, AsyncIterable
from fastapi import Depends
from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession
from app.abstractions.blogs import IBlogsRepository
from app.abstractions.uow import IUnitOfWork
from app.adapters.blogs import SqlalchemyBlogsRepository
from app.adapters.uow import SqlalchemyUnitOfWork
from app.services.blogs import BlogsService
from app.di.dep_collector import collector

@collector.factory(AsyncEngine)
@singleton_factory()
def create_engine() -> AsyncEngine:
    return create_async_engine(settings.DATABASE_URL, echo=settings.ECHO)


@singleton_factory(async_sessionmaker)
def create_session_maker(
    engine: Annotated[AsyncEngine, Depends(Stub(AsyncEngine))],
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)

@collector.factory(AsyncSession)
async def new_session(
    session_maker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(Stub(async_sessionmaker[AsyncSession])),
    ],
) -> AsyncIterable[AsyncSession]:
    async with session_maker() as session:
        yield session



@collector.factory(IUnitOfWork)
def new_unit_of_work(
    session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> IUnitOfWork:
    return SqlalchemyUnitOfWork(session)

@collector.factory(IBlogsRepository)
def new_blog_repository(
    session: Annotated[AsyncSession, Depends(Stub(AsyncSession))],
) -> IBlogsRepository:
    return SqlalchemyBlogsRepository(session)

@collector.factory(BlogsService)
def new_blog_service(
    uow: Annotated[IUnitOfWork, Depends()],
    blogs_repo: Annotated[IBlogsRepository, Depends()],
) -> BlogsService:
    return BlogsService(uow, blogs_repo)

