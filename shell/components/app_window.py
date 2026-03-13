# shell/components/app_window.py
from PyQt6.QtWidgets import QMainWindow, QListWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class AppWindow(QMainWindow):
    def __init__(self, name, parent=None, panel=None):
        super().__init__(parent)
        self.name = name
        self.panel = panel
        self.setWindowTitle(name)
        self.resize(400, 300)

        # Widget central con layout vertical
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # Lista de ventanas abiertas
        self.open_apps_list = QListWidget()
        layout.addWidget(self.open_apps_list)

        # Registrar ventana en el panel
        if self.panel:
            self.panel.register_window(self)
            self.update_open_apps()

    def update_open_apps(self):
        """Actualizar lista de apps abiertas desde el panel"""
        self.open_apps_list.clear()
        if self.panel:
            for app_name in self.panel.open_windows:
                self.open_apps_list.addItem(app_name)

    def closeEvent(self, event):
        # Notificar al panel y actualizar lista de ventanas abiertas
        if self.panel:
            self.panel.close_window(self)
        event.accept()
