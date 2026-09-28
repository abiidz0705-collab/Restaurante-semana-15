import json
from pathlib import Path

class ArchivoServicio:
    def __init__(self):
        self.ruta_datos = Path(__file__).resolve().parent.parent / "datos"
        self.ruta_datos.mkdir(exist_ok=True)
        self.archivo_productos = self.ruta_datos / "productos.json"
        self.archivo_usuarios = self.ruta_datos / "usuarios.json"
        self.archivo_ventas = self.ruta_datos / "ventas.json"

    def cargar_productos(self):
        if not self.archivo_productos.exists():
            return []
        try:
            with open(self.archivo_productos, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            return []

    def guardar_productos(self, lista_productos):
        try:
            with open(self.archivo_productos, "w", encoding="utf-8") as f:
                json.dump(lista_productos, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar productos: {e}")

    def cargar_usuarios(self):
        if not self.archivo_usuarios.exists():
            return []
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")
            return []

    def guardar_usuarios(self, lista_usuarios):
        try:
            with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                json.dump(lista_usuarios, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")

    def cargar_ventas(self):
        if not self.archivo_ventas.exists():
            return []
        try:
            with open(self.archivo_ventas, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar ventas: {e}")
            return []

    def guardar_ventas(self, lista_ventas):
        try:
            with open(self.archivo_ventas, "w", encoding="utf-8") as f:
                json.dump(lista_ventas, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar ventas: {e}")
