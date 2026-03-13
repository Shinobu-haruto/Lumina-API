import os
import configparser
import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QScrollArea
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QIcon, QFont

class MenuItem:
    def __init__(self, name, callback=None, icon_path=None):
        self.name = name
        self.callback = callback
        self.icon_path = icon_path

    def activate(self):
        if callable(self.callback):
            try:
                self.callback()
            except Exception as e:
                print(f"[MenuItem] Error ejecutando {self.name}: {e}")

class MenuCategory:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item: MenuItem):
        self.items.append(item)

class LuminaStartMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(440, 640)
        self.setStyleSheet("background-color: #2a2a2a; color: white; font-family: Arial, sans-serif;")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar aplicaciones...")
        self.search_bar.setStyleSheet("padding:6px; border-radius:8px; background-color:#3a3a3a; color:white;")
        self.search_bar.textChanged.connect(self.update_search)
        self.main_layout.addWidget(self.search_bar)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)
        self.item_widgets = []

        # Fade animation
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Control buttons
        self.ctrl_layout = QHBoxLayout()
        self.main_layout.addLayout(self.ctrl_layout)
        self.control_buttons = []

    def toggle(self):
        if self.isVisible():
            try: self.anim.finished.disconnect(self.hide)
            except Exception: pass
            self.anim.setStartValue(1.0)
            self.anim.setEndValue(0.0)
            self.anim.finished.connect(self.hide)
            self.anim.start()
        else:
            self.setWindowOpacity(0.0)
            self.show()
            try: self.anim.finished.disconnect(self.hide)
            except Exception: pass
            self.anim.setStartValue(0.0)
            self.anim.setEndValue(1.0)
            self.anim.start()

    def add_category(self, category: MenuCategory):
        # Limpia layout
        for w in self.item_widgets:
            w.setParent(None)
        self.item_widgets.clear()

        label = QLabel(category.name)
        label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label.setStyleSheet("margin-top:10px;")
        self.scroll_layout.addWidget(label)
        self.item_widgets.append(label)

        for item in category.items:
            btn = QPushButton(item.name)
            btn.setFixedHeight(36)
            btn.setStyleSheet(
                "text-align:left; padding-left:8px; border-radius:6px; background-color:#3a3a3a;"
                "QPushButton:hover { background-color:#505050; }"
            )
            if item.icon_path:
                btn.setIcon(QIcon(item.icon_path))
                btn.setIconSize(QSize(24,24))
            btn.clicked.connect(item.activate)
            self.scroll_layout.addWidget(btn)
            self.item_widgets.append(btn)

    def update_search(self, text):
        text = text.lower()
        for w in self.item_widgets:
            if isinstance(w, QPushButton):
                w.setVisible(text in w.text().lower())
            elif isinstance(w, QLabel):
                cat_visible = any(
                    isinstance(cw, QPushButton) and text in cw.text().lower()
                    for cw in self.item_widgets[self.item_widgets.index(w)+1:]
                )
                w.setVisible(cat_visible)

    # -------------------------
    # Leer apps Linux
    # -------------------------
    def load_linux_apps(self):
        apps = []
        dirs = ["/usr/share/applications", os.path.expanduser("~/.local/share/applications")]
        for d in dirs:
            if not os.path.exists(d):
                continue
            for f in os.listdir(d):
                if not f.endswith(".desktop"):
                    continue
                full = os.path.join(d, f)
                parser = configparser.ConfigParser(interpolation=None)
                try:
                    parser.read(full, encoding="utf-8")
                except Exception:
                    continue
                if "Desktop Entry" not in parser:
                    continue
                entry = parser["Desktop Entry"]
                if entry.get("NoDisplay", "false").lower() == "true":
                    continue
                name = entry.get("Name")
                exec_cmd = entry.get("Exec")
                icon_name = entry.get("Icon")
                if not name or not exec_cmd:
                    continue
                exec_cmd_clean = exec_cmd.split()[0]
                icon_path = self.resolve_icon(icon_name)
                apps.append(MenuItem(name, lambda c=exec_cmd_clean: subprocess.Popen(c, shell=True), icon_path=icon_path))

        cat = MenuCategory("Aplicaciones")
        for item in apps:
            cat.add_item(item)
        self.add_category(cat)

    def resolve_icon(self, icon_name):
        if not icon_name:
            return None
        paths = [
            f"/usr/share/icons/hicolor/48x48/apps/{icon_name}.png",
            f"/usr/share/icons/hicolor/64x64/apps/{icon_name}.png",
            f"/usr/share/pixmaps/{icon_name}.png"
        ]
        for p in paths:
            if os.path.exists(p):
                return p
        return None

    # -------------------------
    # Botones de control
    # -------------------------
    def add_control_buttons(self):
        controls = [
            ("Configuración", lambda: print("Abrir Configuración")),
            ("Cerrar sesión", lambda: os.system("gnome-session-quit --logout --no-prompt")),
            ("Apagar", lambda: os.system("poweroff"))
        ]
        for name, cb in controls:
            btn = QPushButton(name)
            btn.setFixedHeight(36)
            btn.setStyleSheet("text-align:center; border-radius:6px; background-color:#3a3a3a;")
            btn.clicked.connect(cb)
            self.ctrl_layout.addWidget(btn)
            self.control_buttons.append(btn)

# -------------------------
# Inicialización en API
# -------------------------
def init(api):
    menu = LuminaStartMenu()
    menu.load_linux_apps()
    menu.add_control_buttons()
    api.shell.register_component("start_menu", menu)
    print("[StartMenu] apps Linux + botones de control cargados")
