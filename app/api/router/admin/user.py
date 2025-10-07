from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserUpdate,UserData
from app.crud.user import UserCRUD
from app.core.database import get_db
from app.core.security import AuthService
from app.models.user import User

userrouter = APIRouter(prefix="/users", tags=["Admin Users"])

@userrouter.post("/", response_model=UserOut)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(AuthService().get_current_admin)  # Correctly call the method from an instance of AuthService
):
    user_crud = UserCRUD(db)
    if user_crud.get_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    created = user_crud.create(user)
    return {
        "message": "User created successfully",
        "data": created  # FastAPI + Pydantic will auto-convert ORM object to UserData
    }

@userrouter.get("/", response_model=list[UserData])
def get_all_users(db: Session = Depends(get_db),current_user: User = Depends(AuthService().get_current_user)):
    user_crud = UserCRUD(db)
    return user_crud.get_all()

@userrouter.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    user_crud = UserCRUD(db)
    updated_user = user_crud.update(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "message": "User updated successfully",
        "data": updated_user  # FastAPI + Pydantic will auto-convert ORM object to UserData
    }

@userrouter.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_crud = UserCRUD(db)
    deleted_user = user_crud.delete(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
