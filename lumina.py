# lumina.py

from PyQt6.QtWidgets import QApplication
import sys
import types
import requests
from datetime import datetime

from core.registry import ModuleRegistry
from core.services import ServiceManager
from core.events import EventBus
from core.loader import ModuleLoader
from shell.components.start_menu import StartMenu
from shell.components.panel import Panel
from shell.host import LuminaShellHost
from shell.components.app_window import AppWindow

def load_api_from_github(url, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"No se pudo descargar la API: {response.status_code}")
        sys.exit(1)

    module = types.ModuleType("lumina_api_remote")
    exec(response.text, module.__dict__)
    return module

# ------------------------------------------------------
# URL y token (token opcional si el repo es privado)
# ------------------------------------------------------
GITHUB_API_URL = "https://raw.githubusercontent.com/Shinobu-haruto/Lumina-API/main/core/api.py"
GITHUB_TOKEN = None  # si tu repo es privado, pon tu PAT aquí

# ------------------------------------------------------
# Cargar la API remota
# ------------------------------------------------------
remote_api_module = load_api_from_github(GITHUB_API_URL, GITHUB_TOKEN)

# ------------------------------------------------------
# LuminaSystem
# ------------------------------------------------------
class LuminaSystem:

    def __init__(self):

        # núcleo
        self.registry = ModuleRegistry()
        self.services = ServiceManager()
        self.events = EventBus()

        # usar API remota
        self.api = remote_api_module.LuminaAPI(
            self.registry,
            self.services,
            self.events
        )

        # shell
        self.shell = LuminaShellHost(self.api)

        # exponer shell en la API
        self.api.shell = self.shell

        # cargador de módulos
        self.loader = ModuleLoader("modules", self.api)

    def start(self):
        print("Iniciando Lumina Core")
        self.loader.load_all()
        self.shell.start()

# ------------------------------------------------------
# Bloque principal
# ------------------------------------------------------
if __name__ == "__main__":

    app = QApplication(sys.argv)

    # inicializar sistema
    system = LuminaSystem()
    system.start()

    # crear Start Menu
    start_menu = StartMenu()

    # crear Panel con botón inicio
    panel = Panel(start_menu_component=start_menu)
    panel.show()

    # registrar componentes
    system.shell.register_component("start_menu", start_menu)
    system.shell.register_component("panel", panel)

    # prueba: abrir menú automáticamente al iniciar
    system.events.emit("toggle_start_menu")

    # crear ventanas de prueba
    app1 = AppWindow("Navegador")
    app2 = AppWindow("Editor")
    app3 = AppWindow("Terminal")

    for win in [app1, app2, app3]:
        win.show()
        panel.register_window(win)

    sys.exit(app.exec())
