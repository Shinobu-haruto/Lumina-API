class LuminaWindow:

    def __init__(self, xwindow):

        self.window = xwindow

    def move(self, x, y):

        self.window.configure(x=x, y=y)

    def resize(self, w, h):

        self.window.configure(width=w, height=h)

    def focus(self):

        self.window.set_input_focus()
