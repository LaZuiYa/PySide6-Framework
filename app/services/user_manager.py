from __future__ import annotations
from typing import Optional, Callable, List
from app.db.models import User


class UserManager:
    """
    全局用户管理器，使用单例模式
    """
    _instance = None
    _current_user: Optional[User] = None
    _user_change_callbacks: List[Callable[[Optional[User]], None]] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "UserManager":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_current_user(self, user: Optional[User]) -> None:
        """设置当前用户"""
        self._current_user = user
        # 通知所有回调函数
        for callback in self._user_change_callbacks:
            callback(user)

    def get_current_user(self) -> Optional[User]:
        """获取当前用户"""
        return self._current_user

    def add_user_change_callback(self, callback: Callable[[Optional[User]], None]) -> None:
        """添加用户变更回调函数"""
        self._user_change_callbacks.append(callback)

    def remove_user_change_callback(self, callback: Callable[[Optional[User]], None]) -> None:
        """移除用户变更回调函数"""
        if callback in self._user_change_callbacks:
            self._user_change_callbacks.remove(callback)

    def is_logged_in(self) -> bool:
        """检查用户是否已登录"""
        return self._current_user is not None

    def is_admin(self) -> bool:
        """检查当前用户是否为管理员"""
        return self._current_user is not None and self._current_user.username == "admin"