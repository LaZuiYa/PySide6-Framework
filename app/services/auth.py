from __future__ import annotations

import hashlib
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User, Menu
from app.services.casbin_enforcer import get_enforcer, reload_enforcer

_SALT = "pyside6.framework.salt.v1"  # 简单盐，生产请替换


def hash_password(raw: str) -> str:
    data = (raw + _SALT).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def verify_password(raw: str, password_hash: str) -> bool:
    return hash_password(raw) == password_hash


def authenticate(session: Session, username: str, password: str) -> User | None:
    user = session.scalar(select(User).where(User.username == username))
    if user is None:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def user_accessible_menus(session: Session, user: User) -> list[Menu]:
    """仅基于 Casbin 判定：对每个菜单执行 e.enforce(username, route, "view").
    Casbin 会自动根据 g 关系判断角色，无需从数据库读取角色。
    """
    reload_enforcer()
    e = get_enforcer()
    username = user.username

    menus = session.query(Menu).all()
    result: list[Menu] = []
    for menu in menus:
        if e.enforce(username, menu.route_key, "view"):
            result.append(menu)
    return result
