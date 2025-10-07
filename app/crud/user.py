from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserOut,UserUpdate
from app.core.security import AuthService
class UserCRUD:
    def __init__(self, db: Session, auth_service: AuthService = AuthService()):
        self.db = db
        self.auth_service = auth_service  # Assign here

    def get(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user: UserCreate):
        hashed_password = self.auth_service.hash_password(user.password)  # Now this works
        print(f"Hashing password: {user.password} (length {len(user.password)})")
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            is_active=user.is_active,
            is_admin=user.is_admin
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_data: UserUpdate):
        db_user = self.get(user_id)
        if not db_user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = self.auth_service.hash_password(update_data.pop("password"))

        for key, value in update_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int):
        db_user = self.get(user_id)
        if not db_user:
            return None
        self.db.delete(db_user)
        self.db.commit()
        return db_user
