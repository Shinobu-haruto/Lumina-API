from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication


class StartMenu(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lumina Start")
        self.setFixedSize(320, 420)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )

        layout = QVBoxLayout()

        title = QLabel("Lumina")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn1 = QPushButton("Archivos")
        btn2 = QPushButton("Configuración")
        btn3 = QPushButton("Apagar")

        layout.addWidget(title)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        self.setLayout(layout)

        self.position_menu()

    def position_menu(self):

        screen = QGuiApplication.primaryScreen().geometry()

        x = 10
        y = screen.height() - self.height() - 10

        self.move(x, y)

    def toggle(self):

        if self.isVisible():
            self.hide()
        else:
            self.show()
