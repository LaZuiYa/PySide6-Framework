from __future__ import annotations
from PySide6.QtWidgets import QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QInputDialog, QMessageBox, QLabel, \
    QTreeWidget, QTreeWidgetItem, QPushButton
from qfluentwidgets import TableWidget, PrimaryPushButton, InfoBar

from app.db.base import session_scope
from app.services.system.systemPermissionService import (
    list_roles,
    list_users,
    assign_role_to_user,
    remove_role_from_user,
    get_user_roles,
    assign_permission_to_user,
    remove_permission_from_user,
    get_user_permissions,
    assign_permission_to_role,
    remove_permission_from_role,
    get_role_permissions,
    get_user_all_menu_permissions,
    create_role,
    delete_role,
    set_role_permissions,
    set_user_roles
)
from app.services.system.systemMenuService import list_menus
from app.ui.utils.custonDialog import show_multi_selection_dialog


class SystemPermissionPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("PermissionManagePage")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("RBAC授权（全部基于casbin_rule，支持角色和用户权限的分配与回收）"))

        self.role_tree = QTreeWidget(self)
        self.role_tree.setColumnCount(2)
        self.role_tree.setHeaderLabels(["角色/权限", "动作"])
        self.role_tree.setWordWrap(True)
        # self.role_tree.verticalHeader().setVisible(False)
        self.role_tree.setSelectionBehavior(QTreeWidget.SelectRows)
        layout.addWidget(QLabel("所有角色及其菜单权限（p, role, menu, view）"))

        # 添加角色操作按钮
        role_btn_layout = QHBoxLayout()
        self.btn_add_role = PrimaryPushButton("新增角色")
        self.btn_delete_role = PrimaryPushButton("删除角色")
        self.btn_edit_role_perms = PrimaryPushButton("编辑角色权限")
        self.fresh_role_btn = PrimaryPushButton("刷新")
        self.btn_add_role.clicked.connect(self._add_role)
        self.btn_delete_role.clicked.connect(self._delete_role)
        self.btn_edit_role_perms.clicked.connect(self._edit_role_permissions)
        self.fresh_role_btn.clicked.connect(self.refresh_roles)
        for btn in (self.btn_add_role, self.btn_delete_role, self.btn_edit_role_perms, self.fresh_role_btn):
            role_btn_layout.addWidget(btn)
        role_btn_layout.addStretch()
        layout.addLayout(role_btn_layout)
        layout.addWidget(self.role_tree)

        self.user_table = TableWidget(self)
        self.user_table.setColumnCount(2)
        self.user_table.setHorizontalHeaderLabels(["用户名", "已分配角色"])
        self.user_table.horizontalHeader().setStretchLastSection(True)  # 最后一列自动拉伸
        self.user_table.setWordWrap(True)  # 允许文字换行
        self.user_table.verticalHeader().setVisible(False)  # 隐藏行号
        # 设置选择整行
        self.user_table.setSelectionBehavior(TableWidget.SelectRows)
        # 设置表格高度适应内容
        self.user_table.verticalHeader().setDefaultSectionSize(40)
        layout.addWidget(QLabel("所有用户、其角色、持有全部菜单权限"))

        # 添加用户操作按钮
        user_btn_layout = QHBoxLayout()
        self.btn_add_user_role = PrimaryPushButton("用户授权角色")
        self.btn_remove_user_role = PrimaryPushButton("撤销用户角色")
        self.btn_edit_user_roles = PrimaryPushButton("编辑用户角色")
        self.btn_add_user_role.clicked.connect(self._assign_role)
        self.btn_remove_user_role.clicked.connect(self._revoke_role)
        self.btn_edit_user_roles.clicked.connect(self._edit_user_roles)
        for btn in (self.btn_add_user_role, self.btn_remove_user_role, self.btn_edit_user_roles):
            user_btn_layout.addWidget(btn)
        user_btn_layout.addStretch()
        layout.addLayout(user_btn_layout)
        layout.addWidget(self.user_table)


        self.refresh()

    def refresh_roles(self):
        """刷新角色权限树"""
        self.role_tree.clear()
        roles = list_roles()

        for role in roles:
            # 创建角色节点
            role_item = QTreeWidgetItem(self.role_tree)
            role_item.setText(0, role)
            role_item.setText(1, "")
            role_item.setExpanded(True)  # 默认展开

            # 获取角色权限并添加为子节点
            perms = get_role_permissions(role)
            for perm in perms:
                perm_item = QTreeWidgetItem(role_item)
                perm_item.setText(0, perm[1])  # 菜单路径
                perm_item.setText(1, perm[2])  # 动作

            # 如果没有权限，显示提示
            if not perms:
                empty_item = QTreeWidgetItem(role_item)
                empty_item.setText(0, "无权限")
                empty_item.setDisabled(True)

    def refresh(self):
        # 刷新角色树
        self.refresh_roles()
        # 用户表
        self.user_table.setRowCount(0)
        users = list_users()
        for user in users:
            row = self.user_table.rowCount()
            self.user_table.insertRow(row)
            roles4user = get_user_roles(user)

            self.user_table.setItem(row, 0, QTableWidgetItem(user))
            self.user_table.setItem(row, 1, QTableWidgetItem(", ".join(roles4user)))


    # 新增角色相关方法
    def _add_role(self):
        role_name, ok = QInputDialog.getText(self, "新增角色", "请输入角色名称:")
        if ok and role_name:
            # 创建角色
            create_role(role_name)
            self.refresh()
            InfoBar.success("成功", f"角色 '{role_name}' 已添加", parent=self, duration=2000)

    def _delete_role(self):
        roles = list_roles()
        if not roles:
            InfoBar.info("提示", "当前没有可删除的角色", parent=self)
            return
            
        role_name, ok = QInputDialog.getItem(self, "删除角色", "请选择要删除的角色:", roles, editable=False)
        if not ok or not role_name:
            return
            
        # 确认删除
        confirm = QMessageBox.question(self, "确认删除", f"确定要删除角色 '{role_name}' 吗？这将移除所有与该角色相关的权限。")
        if confirm != QMessageBox.Yes:
            return
            
        # 删除角色
        delete_role(role_name)
        
        self.refresh()
        InfoBar.success("成功", f"角色 '{role_name}' 已删除", parent=self, duration=2000)

    def _edit_role_permissions(self):
        roles = list_roles()
        if not roles:
            InfoBar.info("提示", "当前没有角色可供编辑", parent=self)
            return

        role_name, ok = QInputDialog.getItem(self, "编辑角色权限", "请选择角色:", roles, editable=False)
        if not ok or not role_name:
            return

        # 获取当前角色权限
        current_perms = get_role_permissions(role_name)
        current_perm_strings = [f"{p[1]}" for p in current_perms]  # 只取menu部分

        # 获取所有菜单项
        with session_scope() as s:
            menus = [m.route_key for m in list_menus(s)]

        # 让用户选择菜单权限
        selected_menus, ok = show_multi_selection_dialog(
            self,
            "编辑角色权限",
            f"为角色 '{role_name}' 选择菜单权限:",
            menus,
            [menu for menu in menus if menu in current_perm_strings]
        )

        if not ok:
            return

        # 构造权限列表 [(menu, act), ...]
        permissions = [(menu, "view") for menu in selected_menus]

        # 设置角色权限
        set_role_permissions(role_name, permissions)

        self.refresh()
        InfoBar.success("成功", f"角色 '{role_name}' 的权限已更新", parent=self, duration=2000)
        if hasattr(self.parent(), 'refresh_menus'):
            self.parent().refresh_menus()
    def _edit_user_roles(self):
        users = list_users()
        if not users:
            InfoBar.info("提示", "当前没有用户可供编辑", parent=self)
            return

        user_name, ok = QInputDialog.getItem(self, "编辑用户角色", "请选择用户:", users, editable=False)
        if not ok or not user_name:
            return

        # 获取用户当前角色
        current_roles = get_user_roles(user_name)

        # 获取所有角色
        all_roles = list_roles()

        # 让用户选择角色
        selected_roles, ok = show_multi_selection_dialog(
            self,
            "编辑用户角色",
            f"为用户 '{user_name}' 选择角色:",
            all_roles,
            [role for role in all_roles if role in current_roles]
        )

        if not ok:
            return

        # 设置用户角色
        set_user_roles(user_name, selected_roles)

        self.refresh()
        InfoBar.success("成功", f"用户 '{user_name}' 的角色已更新", parent=self, duration=2000)

    def _assign_role(self):
        users = list_users()
        roles = list_roles()
        user_id, ok = QInputDialog.getItem(self, "授权角色", "选择用户名：", users, editable=False)
        if not ok: return
        role_id, ok = QInputDialog.getItem(self, "授权角色", "选择角色名：", roles, editable=False)
        if not ok: return
        assign_role_to_user(user_id, role_id)
        self.refresh()
        
    def _revoke_role(self):
        users = list_users()
        user_id, ok = QInputDialog.getItem(self, "撤销角色", "选择用户名：", users, editable=False)
        if not ok: return
        roles = get_user_roles(user_id)
        if not roles:
            InfoBar.info("该用户当前无角色", parent=self)
            return
        role, ok = QInputDialog.getItem(self, "撤销角色", "选择角色：", roles, editable=False)
        if not ok: return
        remove_role_from_user(user_id, role)
        self.refresh()
