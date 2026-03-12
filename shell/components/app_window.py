# shell/components/app_window.py

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class AppWindow(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.setWindowTitle(name)
        self.setFixedSize(300, 200)
        self.setWindowFlags(Qt.WindowType.Window)

        layout = QVBoxLayout()
        label = QLabel(f"Ventana de {name}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)
