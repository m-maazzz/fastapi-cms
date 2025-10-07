from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    security = HTTPBearer()

    # Password hashing
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # Token creation
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode = {"sub": data, "exp": expire}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # --- Dependency: current user ---
    def _get_user_from_token(
        self,
        credentials: HTTPAuthorizationCredentials,
        db: Session
    ) -> User:
        token = credentials.credentials
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user

    # Dependency to get current user
    def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
    ) -> User:
        return self._get_user_from_token(credentials, db)

    # Dependency to get current admin
    def get_current_admin(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
    ) -> User:
        user = self._get_user_from_token(credentials, db)
        if not user.is_admin:  # Ensure the user is an admin
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required"
            )
        return user