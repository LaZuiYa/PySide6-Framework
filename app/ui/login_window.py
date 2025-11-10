from __future__ import annotations

from typing import Callable

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import LineEdit, PasswordLineEdit, PrimaryPushButton, InfoBar, InfoBarPosition, setTheme, Theme

from app.db.base import session_scope
from app.services.auth import authenticate


class LoginWindow(QWidget):
    login_success = Signal(object)  # emits user object

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        setTheme(Theme.AUTO)
        self.setWindowTitle("登录 - PySide6 Framework")

        self.username_edit = LineEdit(self)
        self.username_edit.setPlaceholderText("用户名")

        self.password_edit = PasswordLineEdit(self)
        self.password_edit.setPlaceholderText("密码")

        self.login_btn = PrimaryPushButton("登录", self)
        self.login_btn.clicked.connect(self._on_login_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_btn)
        layout.addStretch(1)

        self.resize(360, 200)

    def _show_message(self, text: str, success: bool = False) -> None:
        InfoBar.success(
            title="成功",
            content=text,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self,
        ) if success else InfoBar.error(
            title="错误",
            content=text,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

    def _on_login_clicked(self) -> None:
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        if not username or not password:
            self._show_message("请输入用户名和密码")
            return
        with session_scope() as s:
            user = authenticate(s, username, password)
        if user is None:
            self._show_message("用户名或密码错误")
            return
        self._show_message("登录成功", success=True)
        self.login_success.emit(user)
