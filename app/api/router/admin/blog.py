# app/routers/blog.py

from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.blog import BlogCreate, BlogUpdate, BlogOut, BlogCreateResponse, BlogListResponse
from app.crud.blog import blog_crud
from app.core.database import get_db
from app.core.security import AuthService   
from app.utlis.file_handler import save_upload_file
from slugify import slugify
from typing import List


router = APIRouter(prefix="/blogs", tags=["Blogs"])
auth_service = AuthService()

# ---- Public Routes ----
@router.get("/", response_model=BlogListResponse)
def list_blogs(
    page: int = 1,
    limit: int = 5,
    ispublished: bool = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    if ispublished is not None:
        blogs, total = blog_crud.get_all(db, ispublished=ispublished, skip=skip, limit=limit)
    else:
        blogs, total = blog_crud.get_all(db, skip=skip, limit=limit)

    return BlogListResponse(
        blogs=[BlogOut.model_validate(blog) for blog in blogs],
        total=total,
        page=page,
        size=len(blogs)
    )


# ---- Admin Routes ----
@router.post("/", response_model=BlogCreateResponse)
def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    is_published: bool = Form(True),
    image: UploadFile = File(None),
    author_name: str = Form(...),
    db: Session = Depends(get_db),
    current_admin=Depends(auth_service.get_current_user)
):
    image_url = None
    if image:
        image_url = save_upload_file(image, subfolder="blogs")

    slug = slugify(title)
    blog_data = BlogCreate(
        title=title,
        slug=slug,
        content=content,
        is_published=is_published,
        image_url=image_url,
        author_name=author_name
    )

    created_blog = blog_crud.create(db, blog_data)
    return {
        "message": "Blog created successfully",
        "blog": created_blog
    }

@router.put("/{blog_id}", response_model=BlogCreateResponse)
def update_blog(
    blog_id: int,
    title: str = Form(None),
    content: str = Form(None),
    is_published: bool = Form(None),
    author_name: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_admin=Depends(auth_service.get_current_user)
):
    update_data = {}

    if title is not None:
        update_data['title'] = title
        update_data['slug'] = slugify(title)
    if content is not None:
        update_data['content'] = content
    if is_published is not None:
        update_data['is_published'] = is_published
    if author_name is not None:
        update_data['author_name'] = author_name
    if image:
        update_data['image_url'] = save_upload_file(image, subfolder="blogs")

    blog_update = BlogUpdate(**update_data)

    db_blog = blog_crud.get(db, blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    updated_blog = blog_crud.update(db, db_blog, blog_update)

    return {
        "message": "Blog updated successfully",
        "blog": updated_blog
    }

@router.delete("/{blog_id}")
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(auth_service.get_current_admin)
):
    deleted = blog_crud.delete(db, blog_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}
