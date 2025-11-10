from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from qfluentwidgets import CardWidget, setFont
from PySide6.QtGui import QFont


class AlgorithmPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AlgorithmManagePage")
        self.init_ui()
    
    def init_ui(self):
        # 主布局
        layout = QVBoxLayout(self)
        
        # 创建卡片容器
        card = CardWidget(self)
        card_layout = QVBoxLayout(card)
        
        # 标题
        title_label = QLabel("算法管理")
        setFont(title_label, 18, QFont.Bold)
        card_layout.addWidget(title_label)
        
        # 算法表格
        self.algorithm_table = QTableWidget()
        self.algorithm_table.setColumnCount(5)
        self.algorithm_table.setHorizontalHeaderLabels(["算法ID", "算法名称", "算法类型", "创建时间", "操作"])
        
        # 设置表格列宽
        self.algorithm_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.algorithm_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.algorithm_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.algorithm_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.algorithm_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        # 添加示例数据
        self.add_algorithm_data()
        
        card_layout.addWidget(self.algorithm_table)
        layout.addWidget(card)
        layout.addStretch()
    
    def add_algorithm_data(self):
        # 示例算法数据
        algorithms = [
            {"id": 1, "name": "LSTM", "type": "深度学习", "created_at": "2024-01-01"},
            {"id": 2, "name": "GRU", "type": "深度学习", "created_at": "2024-01-02"},
            {"id": 3, "name": "Transformer", "type": "深度学习", "created_at": "2024-01-03"},
            {"id": 4, "name": "CNN-LSTM", "type": "混合模型", "created_at": "2024-01-04"},
            {"id": 5, "name": "XGBoost", "type": "机器学习", "created_at": "2024-01-05"},
        ]
        
        self.algorithm_table.setRowCount(len(algorithms))
        
        for row, algo in enumerate(algorithms):
            # 添加基本信息
            self.algorithm_table.setItem(row, 0, QTableWidgetItem(str(algo["id"])))
            self.algorithm_table.setItem(row, 1, QTableWidgetItem(algo["name"]))
            self.algorithm_table.setItem(row, 2, QTableWidgetItem(algo["type"]))
            self.algorithm_table.setItem(row, 3, QTableWidgetItem(algo["created_at"]))
            
            # 添加查看按钮
            view_button = QPushButton("查看")
            view_button.setFixedWidth(60)
            view_button.clicked.connect(lambda checked, a=algo: self.view_algorithm(a))
            self.algorithm_table.setCellWidget(row, 4, view_button)
    
    def view_algorithm(self, algorithm):
        # 这里可以实现算法详情查看逻辑
        print(f"查看算法详情: {algorithm['name']} (ID: {algorithm['id']})")
        
        # 创建一个简单的消息卡片来显示算法详情
        from qfluentwidgets import InfoBar, InfoBarPosition
        from PySide6.QtWidgets import QApplication
        
        details = f"""算法详情:
ID: {algorithm['id']}
名称: {algorithm['name']}
类型: {algorithm['type']}
创建时间: {algorithm['created_at']}
描述: 这是一个用于xx预测的{algorithm['name']}算法模型。"""
        
        InfoBar.info(
            title=algorithm['name'],
            content=details,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000,
            parent=self
        )

# 添加Qt导入，避免运行时错误
from PySide6.QtCore import Qt