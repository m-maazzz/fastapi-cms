from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.core.config import settings
from pydantic import computed_field

class BlogBase(BaseModel):
    title: str
    slug: str
    content: str
    author_name: str
    image_url: Optional[str] = None
    is_published: Optional[bool] = True

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int
    author_name: str
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def full_image_url(self) -> str | None:
        if self.image_url:
            return f"{settings.BASE_URL}{self.image_url}"
        return None

    class Config:
        from_attributes = True

class BlogCreateResponse(BaseModel):
    message: str
    blog: BlogOut

class BlogListResponse(BaseModel):
    message: str = "Blogs retrieved successfully"
    blogs: list[BlogOut]
    total: int
    page: int
    size: int

    
    class Config:
        from_attributes = True