# app/crud/crud_blog.py
from typing import Any, Callable, Dict, List, Optional
from sqlalchemy.orm import Session, Query
from sqlalchemy import asc, desc
from app.models.blog import Blog
from app.schemas.blog import BlogCreate, BlogUpdate
from app.crud.base import CRUDBase

class BlogCRUD(CRUDBase[Blog, BlogCreate, BlogUpdate]):
    def __init__(self, model):
        super().__init__(model)

    def get_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[List[str]] = None,
        group_by: Optional[List[str]] = None,
        extras: Optional[Callable[[Query], Query]] = None
    ) -> List[Blog]:
        query = db.query(self.model)

        if filters:
            query = self._apply_filters(query, filters)

        if group_by:
            group_columns = []
            for field_name in group_by:
                col = getattr(self.model, field_name, None)
                if col is not None:
                    group_columns.append(col)
            if group_columns:
                query = query.group_by(*group_columns)

        if order_by:
            order_columns = []
            for field in order_by:
                desc_order = False
                if field.startswith("-"):
                    desc_order = True
                    field = field[1:]
                col = getattr(self.model, field, None)
                if col is not None:
                    order_columns.append(desc(col) if desc_order else asc(col))
            if order_columns:
                query = query.order_by(*order_columns)

        if extras:
            query = extras(query)

        return query.offset(skip).limit(limit).all()

    def _apply_filters(self, query: Query, filters: Dict[str, Any]) -> Query:
        for key, value in filters.items():
            if value is None:
                continue

            if "__" in key:
                field_name, operator = key.split("__", 1)
            else:
                field_name, operator = key, "eq"

            column = getattr(self.model, field_name, None)
            if not column:
                continue  # Skip invalid fields

            filter_func = {
                "eq": lambda c, v: c == v,
                "ne": lambda c, v: c != v,
                "lt": lambda c, v: c < v,
                "lte": lambda c, v: c <= v,
                "gt": lambda c, v: c > v,
                "gte": lambda c, v: c >= v,
                "like": lambda c, v: c.like(f"%{v}%"),
                "ilike": lambda c, v: c.ilike(f"%{v}%"),
                "in": lambda c, v: c.in_(v) if isinstance(v, (list, tuple)) else False,
                "isnull": lambda c, v: c.is_(None) if v in [True, "true", "True"] else c.isnot(None)
            }.get(operator)

            if filter_func:
                query = query.filter(filter_func(column, value))

        return query
    

blog_crud = BlogCRUD(Blog)