from __future__ import annotations

from PySide6.QtWidgets import QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QInputDialog
from qfluentwidgets import TableWidget, PrimaryPushButton, InfoBar
from app.db.base import session_scope
from app.services.system.systemUserService import list_users, create_user, delete_user, reset_password
from app.services.system.systemPermissionService import list_roles, assign_role_to_user


class SystemUserPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("UserManagePage")
        main_layout = QVBoxLayout(self)
        self.table = TableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "用户名"])
        main_layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_add = PrimaryPushButton("新增用户", self)
        btn_add.clicked.connect(self._on_add)
        btn_del = PrimaryPushButton("删除用户", self)
        btn_del.clicked.connect(self._on_delete)
        btn_reset = PrimaryPushButton("重置密码", self)
        btn_reset.clicked.connect(self._on_reset)
        btn_refresh = PrimaryPushButton("刷新", self)
        btn_refresh.clicked.connect(self.refresh)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_del)
        btn_layout.addWidget(btn_reset)
        btn_layout.addWidget(btn_refresh)


        main_layout.addLayout(btn_layout)
        self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        with session_scope() as s:
            users = list_users(s)
        for user in users:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.table.setItem(row, 1, QTableWidgetItem(user.username))

    def _on_add(self):
        uname, ok = QInputDialog.getText(self, "新增用户", "用户名：")
        if not ok or not uname.strip():
            return
        pwd, ok = QInputDialog.getText(self, "新增用户", "初始密码（默认123456）：")
        if not ok:
            return
        with session_scope() as s:
            user = create_user(s, uname, pwd or "123456")
        # 创建后弹窗角色分配
        roles = list_roles()
        if not roles:
            InfoBar.warning(title="无角色", content="请先到权限管理新增角色组", parent=self)
        else:
            role, ok = QInputDialog.getItem(self, "分配角色", "选择一个角色：", roles, editable=False)
            if ok:
                assign_role_to_user(uname, role)
                InfoBar.success(title="完成", content=f"用户[{uname}]已分配角色[{role}]", parent=self)
        self.refresh()

    def _on_delete(self):
        row = self.table.currentRow()
        if row == -1:
            return
        uid = int(self.table.item(row, 0).text())
        if QMessageBox.question(self, "确认", "确定要删除该用户吗？") == QMessageBox.Yes:
            with session_scope() as s:
                delete_user(s, uid)
            self.refresh()

    def _on_reset(self):
        row = self.table.currentRow()
        if row == -1:
            return
        uid = int(self.table.item(row, 0).text())
        if QMessageBox.question(self, "确认", "将密码重置为123456？") == QMessageBox.Yes:
            with session_scope() as s:
                reset_password(s, uid, "123456")
            InfoBar.success(title="操作成功", content="密码已重置为123456", parent=self)
