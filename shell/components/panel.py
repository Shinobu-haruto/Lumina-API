# shell/components/panel.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QGuiApplication
from datetime import datetime

class Panel(QWidget):
    def __init__(self, start_menu_component=None):
        super().__init__()
        self.start_menu = start_menu_component
        self.open_windows = {}  # name -> window

        # panel sin bordes y siempre encima
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )

        # layout horizontal
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(10)

        # botón Inicio
        self.btn_start = QPushButton("Inicio")
        self.btn_start.clicked.connect(self.toggle_start_menu)
        self.layout.addWidget(self.btn_start)

        # etiqueta de reloj
        self.clock_label = QLabel()
        self.update_clock()
        self.layout.addWidget(self.clock_label)

        self.setLayout(self.layout)

        self.resize_panel()

        # temporizador para actualizar el reloj
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

    def resize_panel(self):
        screen = QGuiApplication.primaryScreen().geometry()
        self.setFixedWidth(screen.width())
        self.setFixedHeight(40)
        self.move(0, screen.height() - self.height())

    def toggle_start_menu(self):
        if self.start_menu:
            self.start_menu.toggle()

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.setText(now)

    def register_window(self, app_window):
        """Agregar ventana a la barra de aplicaciones abiertas"""
        name = app_window.name
        if name in self.open_windows:
            return  # ya registrada

        self.open_windows[name] = app_window

        # botón para cerrar ventana
        btn = QPushButton(name)
        btn.clicked.connect(lambda _, w=app_window: self.close_window(w))
        self.layout.insertWidget(1, btn)  # después del botón Inicio

    def close_window(self, window):
        name = window.name
        if name in self.open_windows:
            window.close()
            self.open_windows.pop(name)
            # eliminar botón del layout
            for i in range(self.layout.count()):
                widget = self.layout.itemAt(i).widget()
                if isinstance(widget, QPushButton) and widget.text() == name:
                    widget.deleteLater()
                    break
