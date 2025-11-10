from __future__ import annotations

from typing import Dict

from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon, setTheme, Theme

from app.ui.pages.placeholder_page import PlaceholderPage
from app.services.auth import user_accessible_menus
from app.db.base import session_scope
from app.db.models import User, Menu
from app.ui.utils.signals import GlobalSignals
from app.services.user_manager import UserManager
import importlib

class MainWindow(FluentWindow):
    def __init__(self, current_user: User, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        setTheme(Theme.AUTO)
        self.setWindowTitle("PySide6 Framework")
        self.resize(1080, 720)
        self.current_user = current_user

        # 设置全局用户管理器中的当前用户
        user_manager = UserManager.get_instance()
        user_manager.set_current_user(current_user)

        # 动态注册页面和菜单树
        self._routes: Dict[str, QWidget] = {}
        self._menu_objs: Dict[str, Menu] = {}
        self._register_pages_and_menus()

        # 连接全局菜单变更信号
        GlobalSignals.get_instance().menu_add.connect(self.update_menu_add)
        GlobalSignals.get_instance().menu_delete.connect(self.update_menu_delete)

    def _register_pages_and_menus(self) -> None:
        # 读取可见菜单
        with session_scope() as s:
            visible_menus = user_accessible_menus(s, self.current_user)
            menu_map = {m.id: m for m in visible_menus}
            self._menu_objs = menu_map

        # 注册路由与页面
        for id, m in self._menu_objs.items():
            route = m.route_key
            parts = route.split('/')
            class_name = ''.join(part[0].upper() + part[1:] for part in parts) + 'Page'

            # 动态导入模块
            try:
                # 构造模块路径，例如: app.ui.pages.system.systemUserPage
                module_path = f"app.ui.pages.{'.'.join(parts[:-1]) if len(parts) > 1 else parts[0]}.{class_name[0].lower()+class_name[1:]}"
                module = importlib.import_module(module_path)
                page_class = getattr(module, class_name)
                page_instance = page_class(self)
            except (ImportError, AttributeError):
                # 如果找不到对应的类，则使用占位符页面
                page_instance = PlaceholderPage(m.name, self)

            self._routes[route] = page_instance

        # 构建树（支持二级，最多2层，后续需递归）
        added = set()
        # 顶部导航
        if "home" in self._routes:
            self.addSubInterface(self._routes["home"], FluentIcon.HOME, "主页", NavigationItemPosition.TOP)
            added.add("home")
        def get_icon_from_string(icon_name: str):
            try:
                return getattr(FluentIcon, icon_name)
            except Exception:
                return FluentIcon.MENU
        # 一级
        for id, m in self._menu_objs.items():
            route = m.route_key
            if m.parent_id is None and route != "home":
                self.addSubInterface(self._routes[route], get_icon_from_string(m.icon), m.name)
                added.add(route)
        # 二级
        for id, m in self._menu_objs.items():
            route = m.route_key
            if m.parent_id:
                parent_menu = self._menu_objs.get(m.parent_id)
                if parent_menu and parent_menu.route_key in self._routes:
                    self.addSubInterface(self._routes[route], get_icon_from_string(m.icon), m.name, parent=self._routes[parent_menu.route_key])
                    added.add(route)

    def update_menu_add(self):
        """刷新导航菜单"""
        self._routes.clear()
        self._menu_objs.clear()
        self._register_pages_and_menus()

    def update_menu_delete(self, route: str):
        self.removeInterface(self._routes[route])
        
