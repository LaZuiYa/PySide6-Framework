from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication

from app.config import config
from app.db.seed import init_db
from app.ui.login_window import LoginWindow
from app.ui.main_window import MainWindow


def main() -> None:
    init_db()
    # seed_admin()

    app = QApplication(sys.argv)
    app.setApplicationName(config.app_title)

    login = LoginWindow()
    main_win = None

    def on_login_success(user: object) -> None:
        nonlocal main_win
        login.close()
        # 传递user到主界面
        main_win = MainWindow(user)
        main_win.show()

    def on_logout() -> None:
        nonlocal main_win, login
        if main_win:
            main_win.logout()
            main_win.close()
            main_win = None
        # 重新显示登录窗口
        login = LoginWindow()
        login.login_success.connect(on_login_success)
        login.show()

    login.login_success.connect(on_login_success)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()