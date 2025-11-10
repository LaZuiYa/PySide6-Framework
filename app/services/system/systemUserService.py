from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import User
from app.services.auth import hash_password

def list_users(session: Session) -> List[User]:
    return session.query(User).all()

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def create_user(session: Session, username: str, password: str) -> User:
    user = User(username=username, password_hash=hash_password(password), is_active=True)
    session.add(user)
    session.commit()
    return user

def update_user(session: Session, user_id: int, new_username: Optional[str] = None, is_active: Optional[bool] = None) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None
    if new_username is not None:
        user.username = new_username
    if is_active is not None:
        user.is_active = is_active
    session.commit()
    return user

def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True

def reset_password(session: Session, user_id: int, new_password: str = "123456") -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    user.password_hash = hash_password(new_password)
    session.commit()
    return True
