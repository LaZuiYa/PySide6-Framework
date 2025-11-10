# app/ui/signals.py
from PySide6.QtCore import QObject, Signal


class GlobalSignals(QObject):

    menu_add = Signal()  # route_key, parent_id
    menu_delete = Signal(str)
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
