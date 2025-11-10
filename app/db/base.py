from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from app.config import get_db_engine


class Base(DeclarativeBase):
    pass


# 延迟获取数据库引擎，确保在需要时才建立连接
def get_engine():
    return get_db_engine()


engine = None
SessionLocal = None


def init_database():
    """初始化数据库连接和会话"""
    global engine, SessionLocal
    if engine is None:
        engine = get_engine()
        SessionLocal = sessionmaker(
            bind=engine, 
            autoflush=False, 
            autocommit=False, 
            expire_on_commit=False, 
            class_=Session
        )
    return engine


@contextmanager
def session_scope() -> Iterator[Session]:
    # 确保数据库已初始化
    if SessionLocal is None:
        init_database()
        
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()