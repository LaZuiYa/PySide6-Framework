from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from qfluentwidgets import CardWidget, setFont
from PySide6.QtGui import QFont


class ComponentPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ComponentManagePage")
        self.init_ui()
    
    def init_ui(self):
        # 主布局
        layout = QVBoxLayout(self)
        
        # 创建卡片容器
        card = CardWidget(self)
        card_layout = QVBoxLayout(card)
        
        # 标题
        title_label = QLabel("构件管理")
        setFont(title_label, 18, QFont.Bold)
        card_layout.addWidget(title_label)
        
        # 构件表格
        self.component_table = QTableWidget()
        self.component_table.setColumnCount(5)
        self.component_table.setHorizontalHeaderLabels(["构件ID", "构件名称", "设备类型", "创建时间", "操作"])
        
        # 设置表格列宽
        self.component_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.component_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.component_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.component_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.component_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        # 添加示例数据
        self.add_component_data()
        
        card_layout.addWidget(self.component_table)
        layout.addWidget(card)
        layout.addStretch()
    
    def add_component_data(self):
        # 示例构件数据
        components = [
            {"id": 1, "name": "构件A", "device_type": "涡轮机", "created_at": "2024-01-01"},
            {"id": 2, "name": "构件B", "device_type": "发电机", "created_at": "2024-01-02"},
            {"id": 3, "name": "构件C", "device_type": "压缩机", "created_at": "2024-01-03"},
            {"id": 4, "name": "构件D", "device_type": "泵组", "created_at": "2024-01-04"},
            {"id": 5, "name": "构件E", "device_type": "变速箱", "created_at": "2024-01-05"},
        ]
        
        self.component_table.setRowCount(len(components))
        
        for row, comp in enumerate(components):
            # 添加基本信息
            self.component_table.setItem(row, 0, QTableWidgetItem(str(comp["id"])))
            self.component_table.setItem(row, 1, QTableWidgetItem(comp["name"]))
            self.component_table.setItem(row, 2, QTableWidgetItem(comp["device_type"]))
            self.component_table.setItem(row, 3, QTableWidgetItem(comp["created_at"]))
            
            # 添加查看按钮
            view_button = QPushButton("查看")
            view_button.setFixedWidth(60)
            view_button.clicked.connect(lambda checked, c=comp: self.view_component(c))
            self.component_table.setCellWidget(row, 4, view_button)
    
    def view_component(self, component):
        # 这里可以实现构件详情查看逻辑
        print(f"查看构件详情: {component['name']} (ID: {component['id']})")
        
        # 创建一个简单的消息卡片来显示构件详情
        from qfluentwidgets import InfoBar, InfoBarPosition
        
        details = f"""构件详情:
ID: {component['id']}
名称: {component['name']}
设备类型: {component['device_type']}
创建时间: {component['created_at']}
状态: 正常运行中
监控参数: 温度、振动、压力"""
        
        InfoBar.info(
            title=component['name'],
            content=details,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000,
            parent=self
        )

# 添加Qt导入，避免运行时错误
from PySide6.QtCore import Qt