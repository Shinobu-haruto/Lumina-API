import sys, os, signal
from PyQt6.QtWidgets import QApplication
from core.registry import ModuleRegistry
from core.services import ServiceManager
from core.events import EventBus
from core.loader import ModuleLoader
from core.api import LuminaAPI

from shell.components.start_menu import LuminaStartMenu
from shell.components.panel_superbar import SuperbarPanel
from shell.host import LuminaShellHost

sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

class LuminaSystem:
    def __init__(self):
        # Núcleo
        self.registry = ModuleRegistry()
        self.services = ServiceManager()
        self.events = EventBus()
        self.api = LuminaAPI(self.registry, self.services, self.events)

        # Shell
        self.shell = LuminaShellHost(self.api)
        self.api.shell = self.shell

        # Loader
        modules_path = os.path.join(os.path.dirname(__file__), "modules")
        self.loader = ModuleLoader(modules_path, self.api)

        # Componentes
        self.start_menu = LuminaStartMenu()
        self.start_menu.load_linux_apps()
        self.start_menu.add_control_buttons()

        self.panel = SuperbarPanel(start_menu_component=self.start_menu)
        self.shell.register_component("start_menu", self.start_menu)
        self.shell.register_component("panel", self.panel)

        QApplication.setQuitOnLastWindowClosed(False)

    def start(self):
        print("Iniciando Lumina Core")
        self.loader.load_all()
        print("Módulos cargados:", self.api.list_modules())

        self.panel.show()
        self.shell.start()
        self.events.emit("lumina.started")
        self.events.emit("toggle_start_menu")

def handle_logout(signum, frame):
    print(f"Señal de logout recibida ({signum}), cerrando Lumina...")
    QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    signal.signal(signal.SIGTERM, handle_logout)
    signal.signal(signal.SIGHUP, handle_logout)

    system = LuminaSystem()
    system.start()
    sys.exit(app.exec())
