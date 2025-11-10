from __future__ import annotations

from functools import partial
from typing import Dict, List

from PySide6.QtWidgets import (QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QTreeWidget, QTreeWidgetItem,
                               QInputDialog, QMessageBox, QHeaderView, QFileDialog)
from qfluentwidgets import (TableWidget, PrimaryPushButton, InfoBar,
                            InfoBarPosition, LineEdit, ToolButton)
from qfluentwidgets import FluentIcon

from app.db.base import session_scope
from app.db.models import User
from app.services.modelService import (list_user_models, delete_model,
                                       toggle_model_visibility, save_trained_model,
                                       upload_model_file, download_model_file)
from app.services.user_manager import UserManager


class ModelPage(QWidget):
    """
    模型域管理页面

    功能：
    1. 每个用户独立维护一个文件目录，保存训练的模型结果（存储在远程服务器上）
    2. 用户可以对模型进行权限操作（公开/私有）
    3. 用户可以在自己的文件目录下创建多个目录
    4. 管理员可以看见所有用户的目录
    5. 提供接口：当用户在模型训练完成后将模型保存在自己目录下
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_item = None

        # 从全局用户管理器获取当前用户
        user_manager = UserManager.get_instance()
        self.current_user = user_manager.get_current_user()

        # 添加用户变更回调
        user_manager.add_user_change_callback(self._on_user_changed)

        self.setObjectName("ModelDomainPage")
        self.init_ui()

    def _on_user_changed(self, user: User):
        """当用户变更时调用"""
        self.current_user = user
        self.refresh_view()

    def init_ui(self):
        """初始化UI界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # 页面标题
        title_layout = QHBoxLayout()
        title_label = QLabel("模型域管理")
        title_label.setObjectName("PageTitle")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)

        # 用户信息区域
        user_info_layout = QHBoxLayout()
        self.user_info_label = QLabel("当前用户: 未登录")
        user_info_layout.addWidget(self.user_info_label)
        user_info_layout.addStretch()
        main_layout.addLayout(user_info_layout)

        # 目录操作按钮
        dir_action_layout = QHBoxLayout()

        self.upload_model_btn = PrimaryPushButton(FluentIcon.ADD_TO, "上传模型")
        self.upload_model_btn.clicked.connect(self.upload_model)

        self.refresh_btn = ToolButton(FluentIcon.SYNC)
        self.refresh_btn.setToolTip("刷新")
        self.refresh_btn.clicked.connect(self.refresh_view)

        dir_action_layout.addWidget(self.upload_model_btn)
        dir_action_layout.addStretch()
        dir_action_layout.addWidget(self.refresh_btn)
        main_layout.addLayout(dir_action_layout)

        # 模型列表
        model_card_layout = QVBoxLayout()
        model_card_layout.setSpacing(10)

        model_title_layout = QHBoxLayout()
        model_title_label = QLabel("模型列表")
        model_title_layout.addWidget(model_title_label)
        model_title_layout.addStretch()
        model_card_layout.addLayout(model_title_layout)

        self.model_table = TableWidget()
        self.model_table.setColumnCount(5)
        self.model_table.setHorizontalHeaderLabels(["模型名称", "描述", "大小", "权限", "操作"])
        self.model_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        model_card_layout.addWidget(self.model_table)

        main_layout.addLayout(model_card_layout)
        main_layout.addStretch()
        self.refresh_view()

    def refresh_view(self):
        """刷新视图"""
        if not self.current_user:
            self.user_info_label.setText("当前用户: 未登录")
            return

        self.user_info_label.setText(f"当前用户: {self.current_user.username}")
        self.load_model_list()

    def load_model_list(self):
        """加载模型列表"""
        self.model_table.setRowCount(0)

        if not self.current_user:
            return

        with session_scope() as session:
            models = list_user_models(session, self.current_user.id)

        self.model_table.setRowCount(len(models))
        for row, model in enumerate(models):
            self.model_table.setItem(row, 0, QTableWidgetItem(model.name))
            self.model_table.setItem(row, 1, QTableWidgetItem(model.description or ""))
            self.model_table.setItem(row, 2, QTableWidgetItem(self.format_file_size(model.file_size)))

            # 权限状态
            perm_item = QTableWidgetItem("公开" if model.is_public else "私有")
            self.model_table.setItem(row, 3, perm_item)

            # 操作按钮
            btn_layout = QHBoxLayout()

            download_btn = ToolButton(FluentIcon.DOWN)
            download_btn.setToolTip("下载模型")
            download_btn.clicked.connect(partial(self.download_model, model))

            toggle_perm_btn = ToolButton(FluentIcon.SHARE)
            toggle_perm_btn.setToolTip("切换权限")
            toggle_perm_btn.clicked.connect(partial(self.toggle_model_permission, model))

            delete_btn = ToolButton(FluentIcon.DELETE)
            delete_btn.setToolTip("删除模型")
            delete_btn.clicked.connect(partial(self.delete_model, model))

            btn_layout.addWidget(download_btn)
            btn_layout.addWidget(toggle_perm_btn)
            btn_layout.addWidget(delete_btn)
            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)
            self.model_table.setCellWidget(row, 4, btn_widget)

    def upload_model(self):
        """上传模型文件"""
        if not self.current_user:
            InfoBar.warning(
                title="操作失败",
                content="请先登录",
                parent=self,
                position=InfoBarPosition.TOP_RIGHT
            )
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择模型文件",
            "",
            "模型文件 (*.h5 *.pt *.pth *.pkl *.onnx);;所有文件 (*)"
        )

        if not file_path:
            return

        # 获取模型描述
        description, ok = QInputDialog.getText(self, "模型描述", "请输入模型描述（可选）:")
        if not ok:
            description = None

        # 上传模型文件
        try:
            with session_scope() as session:
                model = upload_model_file(
                    session=session,
                    user=self.current_user,
                    local_file_path=file_path,
                    description=description
                )

            InfoBar.success(
                title="上传成功",
                content=f"模型文件 '{model.name}' 已上传并记录",
                parent=self,
                position=InfoBarPosition.TOP_RIGHT
            )
            self.refresh_view()
        except Exception as e:
            InfoBar.error(
                title="上传失败",
                content=f"上传模型文件时发生错误: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP_RIGHT
            )

    def download_model(self, model):
        """下载模型文件"""
        if not self.current_user:
            InfoBar.warning(
                title="操作失败",
                content="请先登录",
                parent=self,
                position=InfoBarPosition.TOP_RIGHT
            )
            return

        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存模型文件",
            model.name,
            "模型文件 (*.h5 *.pt *.pth *.pkl *.onnx);;所有文件 (*)"
        )

        if not file_path:
            return

        # 下载模型文件
        try:
            with session_scope() as session:
                success = download_model_file(
                    session=session,
                    user=self.current_user,
                    model_id=model.id,
                    local_file_path=file_path
                )

            if success:
                InfoBar.success(
                    title="下载成功",
                    content=f"模型文件 '{model.name}' 已下载到 {file_path}",
                    parent=self,
                    position=InfoBarPosition.TOP_RIGHT
                )
            else:
                InfoBar.error(
                    title="下载失败",
                    content=f"下载模型文件 '{model.name}' 失败",
                    parent=self,
                    position=InfoBarPosition.TOP_RIGHT
                )
        except Exception as e:
            InfoBar.error(
                title="下载失败",
                content=f"下载模型文件时发生错误: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP_RIGHT
            )

    def toggle_model_permission(self, model):
        """切换模型权限"""
        try:
            with session_scope() as session:
                is_public = toggle_model_visibility(session, model.id)

            new_perm = "公开" if is_public else "私有"
            InfoBar.success(
                title="权限更新",
                content=f"模型 '{model.name}' 权限已更改为: {new_perm}",
                parent=self,
                position=InfoBarPosition.TOP_RIGHT
            )
            self.refresh_view()
        except Exception as e:
            InfoBar.error(
                title="权限更新失败",
                content=f"更新权限时发生错误: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP_RIGHT
            )

    def delete_model(self, model):
        """删除模型"""
        reply = QMessageBox.question(
            self,
            '确认删除',
            f"确定要删除模型 '{model.name}' 吗？此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                with session_scope() as session:
                    delete_model(session, model.id)

                InfoBar.success(
                    title="删除成功",
                    content=f"模型 '{model.name}' 已删除",
                    parent=self,
                    position=InfoBarPosition.TOP_RIGHT
                )
                self.refresh_view()
            except Exception as e:
                InfoBar.error(
                    title="删除失败",
                    content=f"删除模型时发生错误: {str(e)}",
                    parent=self,
                    position=InfoBarPosition.TOP_RIGHT
                )

    def is_admin(self) -> bool:
        """判断当前用户是否为管理员"""
        # 从全局用户管理器获取用户信息
        user_manager = UserManager.get_instance()
        return user_manager.is_admin()

    def save_trained_model(self, model_name: str, model_data: bytes, sub_directory: str = "", description: str = None):
        """
        保存训练好的模型到远程服务器

        Args:
            model_name: 模型名称
            model_data: 模型数据（字节）
            sub_directory: 子目录路径（可选）
            description: 模型描述（可选）
        """
        if not self.current_user:
            raise ValueError("用户未登录")

        try:
            with session_scope() as session:
                model = save_trained_model(
                    session=session,
                    user=self.current_user,
                    model_name=model_name,
                    model_data=model_data,
                    sub_directory=sub_directory,
                    description=description
                )

            InfoBar.success(
                title="保存成功",
                content=f"模型 '{model_name}' 已保存",
                parent=self,
                position=InfoBarPosition.TOP_RIGHT
            )
            self.refresh_view()
            return model.id
        except Exception as e:
            InfoBar.error(
                title="保存失败",
                content=f"保存模型时发生错误: {str(e)}",
                parent=self,
                position=InfoBarPosition.TOP_RIGHT
            )
            raise

    def format_file_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.1f} {size_names[i]}"