from Xlib import X, display
from Xlib.protocol import event


class WindowManager:

    def __init__(self, api):

        self.api = api
        self.display = display.Display()
        self.root = self.display.screen().root

        self.windows = []

    def start(self):

        # escuchar eventos de ventanas
        self.root.change_attributes(
            event_mask=
            X.SubstructureRedirectMask |
            X.SubstructureNotifyMask
        )

        print("LuminaWM iniciado")

        while True:
            e = self.display.next_event()
            self.handle_event(e)

    def handle_event(self, e):

        if isinstance(e, event.MapRequest):
            self.manage_window(e.window)

    def manage_window(self, window):

        self.windows.append(window)

        window.map()

        print("Ventana registrada:", window)
