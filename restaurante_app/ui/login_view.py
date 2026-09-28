import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk

class LoginView(ttk.Frame):
    def __init__(self, master, servicio, on_login_success):
        super().__init__(master)
        self.servicio = servicio
        self.on_login_success = on_login_success

        self.ruta_assets = Path(__file__).resolve().parent.parent / "assets"
        self._crear_interfaz()

    def _obtener_ruta_imagen(self, nombres_posibles):
        for nombre in nombres_posibles:
            ruta = self.ruta_assets / nombre
            if ruta.exists():
                return ruta
        return None

    def _crear_interfaz(self):
        frame_login = ttk.Frame(self, padding=30)
        frame_login.pack(expand=True)

        ruta_logo = self._obtener_ruta_imagen(["logo.png", "logo.png.png"])
        if ruta_logo:
            try:
                img = Image.open(ruta_logo)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                lbl_logo = ttk.Label(frame_login, image=self.logo_img)
                lbl_logo.pack(pady=(0, 20))
            except Exception as e:
                print(f"Error cargando logo: {e}")

        lbl_titulo = ttk.Label(frame_login, text="Bienvenido", font=("Helvetica", 18, "bold"))
        lbl_titulo.pack(pady=(0, 20))

        lbl_user = ttk.Label(frame_login, text="Usuario o ID:", font=("Helvetica", 10))
        lbl_user.pack(anchor="w", pady=(5, 0))
        self.entry_usuario = ttk.Entry(frame_login, font=("Helvetica", 11), width=25)
        self.entry_usuario.pack(fill="x", pady=(0, 15))
        self.entry_usuario.focus()

        lbl_clave = ttk.Label(frame_login, text="Contraseña:", font=("Helvetica", 10))
        lbl_clave.pack(anchor="w", pady=(5, 0))
        self.entry_clave = ttk.Entry(frame_login, show="*", font=("Helvetica", 11), width=25)
        self.entry_clave.pack(fill="x", pady=(0, 20))

        self.entry_clave.bind("<Return>", lambda e: self._ejecutar_login())

        btn_login = ttk.Button(frame_login, text="Iniciar Sesión", command=self._ejecutar_login)
        btn_login.pack(fill="x", ipady=5)

    def _ejecutar_login(self):
        usuario = self.entry_usuario.get().strip()
        clave = self.entry_clave.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Atención", "Por favor ingrese usuario y contraseña.")
            return

        if hasattr(self.servicio, "validar_acceso"):
            exito = self.servicio.validar_acceso(usuario, clave)
        else:
            exito = True

        if exito:
            messagebox.showinfo("Bienvenido", f"Acceso concedido para '{usuario}'.")
            self.on_login_success(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")