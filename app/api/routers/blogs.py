from fastapi import APIRouter, Depends
from app.di.stub import Stub
from app.schemas import blogs as blog_schemes
from typing import Annotated
from app.services.blogs import BlogsService

router = APIRouter(
    prefix="/blogs",
    tags=["BLOGS"]
)

@router.post('/')
async def create_blog(
    blog: blog_schemes.CreateBlogSchema,
    blogs_service: Annotated[BlogsService, Depends(Stub(BlogsService))]
):
    return await blogs_service.save_blog(blog=blog)


@router.get('/{id}')
async def get_blog_by_id(
    id: int,
    blogs_service: Annotated[BlogsService, Depends(Stub(BlogsService))]
) -> blog_schemes.BlogSchema:
    return await blogs_service.get_blog(id=id)
