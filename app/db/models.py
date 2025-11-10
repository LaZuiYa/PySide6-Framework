from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Integer, default=1, nullable=False)
    models: Mapped[List["Model"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Menu(Base, TimestampMixin):
    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    route_key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    icon: Mapped[Optional[str]] = mapped_column(String(64))
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("menu.id", ondelete="SET NULL"))
    children: Mapped[List["Menu"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    parent: Mapped[Optional["Menu"]] = relationship(back_populates="children", remote_side=[id])


class Model(Base, TimestampMixin):
    __tablename__ = "model"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(512))
    file_path: Mapped[str] = mapped_column(String(256), nullable=False)  # 服务器上的文件路径
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    
    # 关系
    owner: Mapped["User"] = relationship(back_populates="models")