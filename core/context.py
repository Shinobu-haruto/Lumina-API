
class LuminaContext:

    def __init__(self, api, module_name):

        self.api = api
        self.module = module_name

    # servicios

    def service(self, name):
        return self.api.services.get(name)

    # eventos

    def emit(self, event, data=None):
        self.api.events.emit(event, data, self.module)

    def subscribe(self, event, callback):
        self.api.events.subscribe(event, callback)

    # logging

    def log(self, message):
        self.api.logger.log(self.module, message)
