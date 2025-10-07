# app/crud/token.py
from sqlalchemy.orm import Session
from app.models.token import UserToken
from datetime import datetime

class TokenCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_refresh_token(self, user_id: int, refresh_token: str, refresh_expires_at: datetime):
        db_token = UserToken(
            user_id=user_id,
            refresh_token=refresh_token,
            refresh_expires_at=refresh_expires_at,
            is_revoked=False
        )
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)
        return db_token

    def get_by_refresh(self, refresh_token: str):
        return self.db.query(UserToken).filter(UserToken.refresh_token == refresh_token).first()

    def revoke(self, token_obj: UserToken):
        token_obj.is_revoked = True
        self.db.commit()
        return token_obj

    def revoke_all_for_user(self, user_id: int):
        tokens = self.db.query(UserToken).filter(UserToken.user_id == user_id, UserToken.is_revoked == False).all()
        for t in tokens:
            t.is_revoked = True
        self.db.commit()
        return tokens
