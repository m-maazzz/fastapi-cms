# app/api/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import LoginRequest, UserCreate, UserOut   
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.crud.user import UserCRUD
from app.core.security import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(form_data : LoginRequest, db: Session = Depends(get_db) ,auth_service: AuthService = Depends()):
    user_crud = UserCRUD(db)
    user = user_crud.get_by_email(form_data.email)
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = auth_service.create_access_token(data=str(user.id))

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    return {"message": "Logged out"}