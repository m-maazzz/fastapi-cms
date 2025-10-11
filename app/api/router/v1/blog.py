from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.blog import BlogCreate, BlogUpdate, BlogOut, BlogCreateResponse, BlogListResponse
from app.crud.blog import blog_crud
from app.core.database import get_db
from app.core.security import AuthService   
from app.utlis.file_handler import save_upload_file
from slugify import slugify
from typing import List, Optional
from fastapi import Query


blog_router = APIRouter(prefix="/blogs", tags=["User-Blogs"])


@blog_router.get("/", response_model=BlogListResponse)
def list_blogs(
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    # Always fetch only published blogs
    blogs, total = blog_crud.get_all(
        db,
        ispublished=True,
        skip=skip,
        limit=limit
    )

    return BlogListResponse(
        blogs=[BlogOut.model_validate(blog) for blog in blogs],
        total=total,
        page=page,
        size=len(blogs)
    )



@blog_router.get("/multi", response_model=BlogListResponse)
def list_blogs_multi(
    page: int = 1,
    limit: int = 10,
    filters: Optional[List[str]] = Query(None, description="Filters like is_published__eq:true,author_name__like:john"),
    order_by: Optional[List[str]] = Query(None, description="Order by fields, prefix '-' for desc, e.g. -created_at"),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * limit

    # Parse filters from list of "key:value" strings into dict
    filter_dict = {}
    if filters:
        for f in filters:
            if ':' in f:
                k, v = f.split(':', 1)
                # Try to convert booleans and ints
                if v.lower() in ("true", "false"):
                    v = v.lower() == "true"
                elif v.isdigit():
                    v = int(v)
                filter_dict[k] = v

    blogs = blog_crud.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        filters=filter_dict if filter_dict else None,
        order_by=order_by
    )

    # Optional: get total count with filters applied
    total_query = db.query(blog_crud.model)
    if filter_dict:
        total_query = blog_crud._apply_filters(total_query, filter_dict)
    total = total_query.count()

    return BlogListResponse(
        blogs=[BlogOut.model_validate(blog) for blog in blogs],
        total=total,
        page=page,
        size=len(blogs)
    )

@blog_router.get("/{id}", response_model=BlogOut)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = blog_crud.get(db, id)
    if not blog or not blog.is_published:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

