import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al sys.path
ruta_raiz = Path(__file__).resolve().parent
sys.path.insert(0, str(ruta_raiz))

import tkinter as tk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Restaurante - Login")
        self.root.geometry("450x450")

        # Cargar icono de la ventana principal si existe
        ruta_ico = ruta_raiz / "assets" / "icon.ico"
        if not ruta_ico.exists():
            ruta_ico = ruta_raiz / "assets" / "icon.ico.ico"
        if ruta_ico.exists():
            try:
                self.root.iconbitmap(str(ruta_ico))
            except Exception:
                pass

        self.servicio = RestauranteServicio()
        self.mostrar_login()

    def mostrar_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.geometry("450x450")
        self.login_view = LoginView(self.root, self.servicio, self.iniciar_aplicacion_principal)
        self.login_view.pack(expand=True, fill="both")

    def iniciar_aplicacion_principal(self, usuario):
        for widget in self.root.winfo_children():
            widget.destroy()
        MainView(self.root, self.servicio, usuario, app_controller=self)

    def reiniciar_a_login(self):
        self.mostrar_login()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()