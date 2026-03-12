class VerticalLayout:

    def apply(self, windows, screen_width, screen_height):

        count = len(windows)

        if count == 0:
            return

        height = screen_height // count

        for i, win in enumerate(windows):

            win.move(0, i * height)
            win.resize(screen_width, height)
