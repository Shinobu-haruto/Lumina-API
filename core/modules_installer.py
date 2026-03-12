import zipfile
import os
import json


class ModuleInstaller:

    def __init__(self, modules_path="modules"):
        self.modules_path = modules_path

    def install(self, package_path):

        if not zipfile.is_zipfile(package_path):
            print("[Installer] Archivo no válido")
            return

        with zipfile.ZipFile(package_path) as z:

            if "manifest.json" not in z.namelist():
                print("[Installer] manifest.json no encontrado")
                return

            manifest = json.loads(z.read("manifest.json"))

            module_id = manifest.get("id")

            target = os.path.join(self.modules_path, module_id)

            print(f"[Installer] Instalando módulo: {module_id}")

            os.makedirs(target, exist_ok=True)

            z.extractall(target)

            print("[Installer] Instalación completada")
