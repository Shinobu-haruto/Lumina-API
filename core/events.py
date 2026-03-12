class EventBus:

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name, callback):
        """Registrar escucha de evento"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []

        self.listeners[event_name].append(callback)

    def unsubscribe(self, event_name, callback):
        if event_name in self.listeners:
            if callback in self.listeners[event_name]:
                self.listeners[event_name].remove(callback)

    def emit(self, event_name, **data):
        """Emitir evento"""
        if event_name not in self.listeners:
            return

        for callback in self.listeners[event_name]:
            try:
                callback(**data)
            except Exception as e:
                print(f"Event error [{event_name}]: {e}")
