import os
import json
import importlib.util


class ModuleLoader:

    def __init__(self, modules_path, api):

        self.modules_path = modules_path
        self.api = api

    def load_all(self):

        print("[ModuleLoader] Buscando módulos")

        if not os.path.exists(self.modules_path):
            print("[ModuleLoader] Carpeta modules no encontrada")
            return

        for folder in os.listdir(self.modules_path):

            module_dir = os.path.join(self.modules_path, folder)
            manifest_path = os.path.join(module_dir, "manifest.json")

            if not os.path.isfile(manifest_path):
                continue

            self.load_module(module_dir, manifest_path)

    def load_module(self, module_dir, manifest_path):

        with open(manifest_path) as f:
            manifest = json.load(f)

        name = manifest.get("name")
        entry = manifest.get("entry")

        entry_path = os.path.join(module_dir, entry)

        print(f"[ModuleLoader] Cargando módulo: {name}")

        spec = importlib.util.spec_from_file_location(name, entry_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "init"):
            module.init(self.api)
