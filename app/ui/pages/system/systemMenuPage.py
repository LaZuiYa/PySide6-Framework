from __future__ import annotations

from PySide6.QtWidgets import QTreeWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox, QLabel, \
    QDialog
from qfluentwidgets import TreeWidget, PrimaryPushButton, FluentIcon
from app.db.base import session_scope
from app.services.system.systemMenuService import menu_tree, create_menu, update_menu, delete_menu

from app.ui.utils.custonDialog import IconSelectorDialog
from app.ui.utils.signals import GlobalSignals


class SystemMenuPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("MenuManagePage")
        layout = QVBoxLayout(self)
        self.tree = TreeWidget(self)

        # 添加以下代码来设置TreeWidget的列
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["ID", "菜单名称", "路由Key", "图标", "更新时间"])

        layout.addWidget(QLabel("菜单树"))
        layout.addWidget(self.tree)
        btns = QHBoxLayout()
        btn_add = PrimaryPushButton("新增菜单", self)
        btn_add.clicked.connect(self._add_menu)
        btn_edit = PrimaryPushButton("编辑菜单", self)
        btn_edit.clicked.connect(self._edit_menu)
        btn_del = PrimaryPushButton("删除菜单", self)
        btn_del.clicked.connect(self._del_menu)
        btn_refresh = PrimaryPushButton("刷新", self)
        btn_refresh.clicked.connect(self.refresh)
        for b in (btn_add, btn_edit, btn_del, btn_refresh):
            btns.addWidget(b)
        layout.addLayout(btns)
        self.refresh()

    def refresh(self):
        self.tree.clear()
        with session_scope() as s:
            tree_data = menu_tree(s)

        def add_items(node_list, parent_item=None):
            for n in node_list:
                item = QTreeWidgetItem([str(n["id"]), n["name"], n["route_key"], n["icon"], n["updated_at"].strftime("%Y-%m-%d %H:%M:%S")])
                try:
                    icon_obj = getattr(FluentIcon, n["icon"]).icon()
                    item.setIcon(3, icon_obj)
                except AttributeError:
                    pass
                if parent_item:
                    parent_item.addChild(item)  # 添加为父节点的子项
                else:
                    self.tree.addTopLevelItem(item)  # 只有根节点才作为顶层项添加

                if n["children"]:
                    add_items(n["children"], item)  # 递归添加子节点

        add_items(tree_data)

    def _add_menu(self):
        name, ok = QInputDialog.getText(self, "新增菜单", "名称：")
        if not ok or not name.strip():
            return
        route, ok = QInputDialog.getText(self, "新增菜单", "唯一路由key：")
        if not ok or not route.strip():
            return

        # 使用自定义图标选择对话框
        dialog = IconSelectorDialog(self)
        if dialog.exec() == QDialog.Accepted:
            icon = dialog.get_selected_icon()
            if not icon:
                return
        else:
            return

        parent = self.tree.currentItem()
        parent_id = int(parent.text(0)) if parent else None
        with session_scope() as s:
            create_menu(s, name, route, icon, parent_id=parent_id)
        self.refresh()

        # 发出全局菜单变更信号
        GlobalSignals.get_instance().menu_add.emit()
    def _edit_menu(self):
        item = self.tree.currentItem()
        if not item:
            return
        menu_id = int(item.text(0))
        name, ok = QInputDialog.getText(self, "编辑菜单", "新名称：")
        if not ok or not name.strip():
            return
        with session_scope() as s:
            update_menu(s, menu_id, name)
        self.refresh()
    def _del_menu(self):
        item = self.tree.currentItem()
        if not item:
            return
        route_key = str(item.text(2))
        if QMessageBox.question(self, "确认", "删除该菜单及其子级？") == QMessageBox.Yes:
            with session_scope() as s:
                delete_menu(s, route_key)
            self.refresh()
            # 发出全局菜单变更信号
            GlobalSignals.get_instance().menu_delete.emit(route_key)
