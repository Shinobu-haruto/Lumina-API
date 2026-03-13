# shell/components/panel_superbar.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QToolButton, QMenu
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QGuiApplication, QIcon, QColor
from datetime import datetime

class SuperbarPanel(QWidget):
    def __init__(self, start_menu_component=None):
        super().__init__()
        self.start_menu = start_menu_component
        self.open_windows = {}  # app_name -> list of windows
        self.window_buttons = {}  # app_name -> QPushButton

        # panel sin bordes y siempre encima
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)

        # layout principal
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)

        # Botón Inicio
        self.btn_start = QPushButton("Inicio")
        self.btn_start.setFixedSize(80, 36)
        self.btn_start.clicked.connect(self.toggle_start_menu)
        self.main_layout.addWidget(self.btn_start)

        # Contenedor de ventanas abiertas
        self.windows_layout = QHBoxLayout()
        self.windows_layout.setSpacing(2)
        self.main_layout.addLayout(self.windows_layout)

        # Espaciador flexible
        self.main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Reloj
        self.clock_label = QLabel()
        self.update_clock()
        self.main_layout.addWidget(self.clock_label)

        self.setLayout(self.main_layout)
        self.resize_panel()

        # Temporizador para actualizar el reloj
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
        """Agregar ventana a la superbar"""
        name = app_window.name
        if name not in self.open_windows:
            self.open_windows[name] = []

            # Crear botón de grupo
            btn = QToolButton()
            btn.setText(name)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #3a3a3a;
                    border-radius: 4px;
                    padding: 4px 8px;
                }
                QToolButton:hover {
                    background-color: #505050;
                }
                QToolButton:checked {
                    background-color: #606060;
                }
            """)
            btn.clicked.connect(lambda checked, n=name: self.focus_window_group(n))
            btn.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
            self.windows_layout.addWidget(btn)
            self.window_buttons[name] = btn

        self.open_windows[name].append(app_window)
        self.focus_window_group(name)

    def focus_window_group(self, name):
        """Al hacer click en el botón, mostrar la última ventana de ese grupo"""
        if name in self.open_windows and self.open_windows[name]:
            window = self.open_windows[name][-1]
            window.show()
            window.raise_()
            window.activateWindow()
            # Actualizar estado del botón
            for btn_name, btn in self.window_buttons.items():
                btn.setChecked(btn_name == name)

    def close_window(self, window):
        name = window.name
        if name in self.open_windows and window in self.open_windows[name]:
            self.open_windows[name].remove(window)
            window.close()
            if not self.open_windows[name]:
                # eliminar botón de grupo si no quedan ventanas
                btn = self.window_buttons.pop(name)
                btn.deleteLater()
                self.open_windows.pop(name)
