class LuminaAPI:

    def __init__(self, registry, services, events, logger=None):

        self.registry = registry
        self.services = services
        self.events = events
        self.logger = logger

    # -----------------------
    # módulos
    # -----------------------

    def register_module(self, name, module):

        self.registry.register(name, module)

        if self.logger:
            self.logger.log("core", f"Module loaded: {name}")

    def get_module(self, name):

        return self.registry.get(name)

    def list_modules(self):

        return self.registry.list()

    # -----------------------
    # eventos
    # -----------------------

    def emit(self, event, data=None):

        if self.logger:
            self.logger.log("event", f"{event}")

        self.events.emit(event, data)

    def subscribe(self, event, callback):

        self.events.subscribe(event, callback)

    # -----------------------
    # servicios
    # -----------------------

    def register_service(self, name, service):

        self.services.register(name, service)

        if self.logger:
            self.logger.log("core", f"Service registered: {name}")

    def get_service(self, name):

        return self.services.get(name)
