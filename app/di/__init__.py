from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    AsyncSession
)
from app.di.providers import (
    create_engine,
    create_session_maker,
    new_session,
    new_blog_repository,
    new_unit_of_work,
    new_blog_service
)
from app.abstractions.uow import IUnitOfWork
from app.abstractions.blogs import IBlogsRepository
from app.services.blogs import BlogsService


def init_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[AsyncEngine] = create_engine
    app.dependency_overrides[async_sessionmaker[AsyncSession]] = create_session_maker
    app.dependency_overrides[AsyncSession] = new_session
    app.dependency_overrides[IUnitOfWork] = new_unit_of_work
    app.dependency_overrides[IBlogsRepository] = new_blog_repository
    app.dependency_overrides[BlogsService] = new_blog_service
    
