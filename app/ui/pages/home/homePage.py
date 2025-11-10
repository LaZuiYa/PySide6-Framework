from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class HomePage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("homeInterface")
        layout = QVBoxLayout(self)
        title = QLabel("欢迎使用 PySide6 Framework")
        
        title.setObjectName("HomeTitle")
        layout.addWidget(title)
        layout.addStretch(1)
