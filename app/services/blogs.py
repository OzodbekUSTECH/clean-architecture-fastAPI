from app.models import Blog
from app.schemas import blogs as blog_schemes
from app.abstractions.blogs import IBlogsRepository
from app.abstractions.uow import IUnitOfWork

class BlogsService:

    def __init__(
            self,
            uow: IUnitOfWork,
            blogs_repo: IBlogsRepository
    ):
        self.uow = uow
        self.blogs_repo = blogs_repo

    async def save_blog(self, blog: blog_schemes.CreateBlogSchema) -> None:
        await self.blogs_repo.save_blog(data=blog.model_dump())
        await self.uow.commit()

    async def get_blog(self, id: int) -> Blog | None:
        return await self.blogs_repo.get_blog(id=id)