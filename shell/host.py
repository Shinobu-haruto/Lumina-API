# shell/host.py

class LuminaShellHost:

    def __init__(self, api):

        # acceso al núcleo de Lumina
        self.api = api
        self.events = api.events
        self.services = api.services
        self.registry = api.registry

        # componentes UI registrados
        self.components = {}

    # -----------------------------
    # registro de componentes UI
    # -----------------------------
    def register_component(self, name, component):

        self.components[name] = component
        print(f"[ShellHost] Componente registrado: {name}")

    # -----------------------------
    # inicio del shell
    # -----------------------------
    def start(self):

        print("[ShellHost] Iniciando Lumina ShellHost")

        self._register_events()

        print("[ShellHost] ShellHost listo")

    # -----------------------------
    # eventos del sistema
    # -----------------------------
    def _register_events(self):

        self.events.subscribe("toggle_start_menu", self.toggle_start_menu)
        self.events.subscribe("show_notifications", self.show_notifications)
        self.events.subscribe("open_quick_settings", self.open_quick_settings)

    # -----------------------------
    # handlers
    # -----------------------------
    def toggle_start_menu(self, data=None):

        menu = self.components.get("start_menu")

        if menu:
            menu.toggle()
        else:
            print("[ShellHost] StartMenu no registrado")

    def show_notifications(self, data=None):

        center = self.components.get("notifications")

        if center:
            center.show()
        else:
            print("[ShellHost] NotificationCenter no registrado")

    def open_quick_settings(self, data=None):

        panel = self.components.get("quick_settings")

        if panel:
            panel.show()
        else:
            print("[ShellHost] QuickSettings no registrado")

    # -----------------------------
    # utilidades
    # -----------------------------
    def list_components(self):

        print("[ShellHost] Componentes activos:")

        for name in self.components:
            print(" -", name)
