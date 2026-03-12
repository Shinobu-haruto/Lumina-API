
class StartMenu:

    def toggle(self):
        print("Start Menu abierto")


def init(api):

    menu = StartMenu()

    api.shell.register_component(
        "start_menu",
        menu
    )

    print("[StartMenu] módulo cargado")
