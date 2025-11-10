from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class PlaceholderPage(QWidget):
    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName(title)
        layout = QVBoxLayout(self)
        label = QLabel(title)
        label.setObjectName("PlaceholderTitle")
        layout.addWidget(label)
        layout.addStretch(1)
