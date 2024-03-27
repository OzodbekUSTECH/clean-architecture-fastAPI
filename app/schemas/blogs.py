from pydantic import BaseModel

class CreateBlogSchema(BaseModel):
    title: str
    description: str

class UpdateBlogSchema(CreateBlogSchema):
    pass

class BlogSchema(UpdateBlogSchema):
    id: int