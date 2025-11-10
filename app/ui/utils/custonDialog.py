from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, \
    QDialogButtonBox, QLabel
from PySide6.QtCore import Qt, QSize
from qfluentwidgets import FluentIcon


class IconSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择图标")
        self.setGeometry(300, 300, 400, 500)

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QSize(24, 24))  # 设置图标大小
        layout.addWidget(self.list_widget)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # 填充图标列表
        self._populate_icons()
        self.selected_icon = None

    def _populate_icons(self):
        # 获取所有 FluentIcon 成员
        icons = [attr for attr in dir(FluentIcon)
                 if not attr.startswith('_') and attr not in ['name', 'value']]

        for icon_name in icons:
            try:
                # 直接使用 FluentIcon 枚举成员作为图标
                icon_obj = getattr(FluentIcon, icon_name)
                # 如果上面的方法不行，尝试以下方式：
                # icon_obj = FluentIcon(icon_name)  # 如果 FluentIcon 支持这种方式
                item = QListWidgetItem(icon_name)  # 如果需要调用 icon() 方法
                item.setIcon(icon_obj.icon())
                item.setData(2, icon_name)  # 存储图标名称
                self.list_widget.addItem(item)
            except Exception as e:
                print(f"无法加载图标 {icon_name}: {e}")  # 打印具体错误信息
                pass

    def get_selected_icon(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            return current_item.data(2)
        return None

def show_multi_selection_dialog(parent, title, label, items, selected_items=None):
    """
    显示一个多选对话框
    """
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    dialog.resize(400, 300)

    layout = QVBoxLayout(dialog)

    # 添加标签
    layout.addWidget(QLabel(label))

    # 创建列表控件
    list_widget = QListWidget()
    for item in items:
        list_item = QListWidgetItem(item)
        list_item.setCheckState(Qt.Checked if selected_items and item in selected_items else Qt.Unchecked)
        list_widget.addItem(list_item)

    layout.addWidget(list_widget)

    # 添加按钮
    button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    button_box.accepted.connect(dialog.accept)
    button_box.rejected.connect(dialog.reject)
    layout.addWidget(button_box)

    if dialog.exec() == QDialog.Accepted:
        # 返回选中的项目
        selected = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())
        return selected, True
    else:
        return None, False  # 用户取消