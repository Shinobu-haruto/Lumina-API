from shellhost.host import LuminaShellHost
from shellhost.start_menu import StartMenu

host = LuminaShellHost()

start_menu = StartMenu()

host.register("start_menu", start_menu)

host.start()
