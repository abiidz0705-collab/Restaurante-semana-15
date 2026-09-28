import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk

class MainView:
    def __init__(self, root, servicio, usuario_actual="admin", app_controller=None):
        self.root = root
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.app_controller = app_controller

        self.root.title("Sistema de Gestión de Restaurante")
        self.root.geometry("900x600")

        self.ruta_assets = Path(__file__).resolve().parent.parent / "assets"

        self._crear_interfaz()
        self._cargar_datos_tablas()

    def _obtener_ruta_imagen(self, nombres_posibles):
        for nombre in nombres_posibles:
            ruta = self.ruta_assets / nombre
            if ruta.exists():
                return ruta
        return None

    def _cargar_icono(self, nombres):
        ruta = self._obtener_ruta_imagen(nombres)
        if ruta:
            try:
                img = Image.open(ruta)
                img = img.resize((20, 20), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error icono: {e}")
        return None

    def _crear_interfaz(self):
        # Frame superior para usuario y botón de cerrar sesión
        frame_top = ttk.Frame(self.root, padding=10)
        frame_top.pack(fill="x", side="top")

        lbl_user = ttk.Label(frame_top, text=f"Usuario activo: {self.usuario_actual}", font=("Helvetica", 10, "bold"))
        lbl_user.pack(side="left")

        btn_logout = ttk.Button(frame_top, text="Cerrar Sesión", command=self._cerrar_sesion)
        btn_logout.pack(side="right")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Iconos de las pestañas
        self.icon_prod = self._cargar_icono(["icon_producto.png", "icon_producto.png.png"])
        self.icon_user = self._cargar_icono(["icon_usuario.png", "icon_usuario.png.png", "usuario.png"])
        self.icon_vent = self._cargar_icono(["icon_venta.png", "icon_venta.png.png"])

        self.tab_productos = ttk.Frame(self.notebook)
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.tab_ventas = ttk.Frame(self.notebook)

        if self.icon_prod:
            self.notebook.add(self.tab_productos, text=" Productos", image=self.icon_prod, compound="left")
        else:
            self.notebook.add(self.tab_productos, text="Productos")

        if self.icon_user:
            self.notebook.add(self.tab_usuarios, text=" Usuarios", image=self.icon_user, compound="left")
        else:
            self.notebook.add(self.tab_usuarios, text="Usuarios")

        if self.icon_vent:
            self.notebook.add(self.tab_ventas, text=" Ventas", image=self.icon_vent, compound="left")
        else:
            self.notebook.add(self.tab_ventas, text="Ventas")

        self._construir_tab_productos()
        self._construir_tab_usuarios()
        self._construir_tab_ventas()

    def _construir_tab_productos(self):
        frame_form = ttk.LabelFrame(self.tab_productos, text="Datos del Producto", padding=10)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frame_form, text="ID Producto:").pack(anchor="w")
        self.ent_p_id = ttk.Entry(frame_form)
        self.ent_p_id.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="Nombre:").pack(anchor="w")
        self.ent_p_nombre = ttk.Entry(frame_form)
        self.ent_p_nombre.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="Precio ($):").pack(anchor="w")
        self.ent_p_precio = ttk.Entry(frame_form)
        self.ent_p_precio.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="Categoría:").pack(anchor="w")
        self.ent_p_cat = ttk.Entry(frame_form)
        self.ent_p_cat.pack(fill="x", pady=(0, 15))

        btn_add = ttk.Button(frame_form, text="Agregar Producto", command=self._guardar_producto)
        btn_add.pack(fill="x", pady=2)

        btn_del = ttk.Button(frame_form, text="Eliminar Producto", command=self._eliminar_producto)
        btn_del.pack(fill="x", pady=2)

        frame_tabla = ttk.Frame(self.tab_productos, padding=10)
        frame_tabla.pack(side="right", expand=True, fill="both")

        cols = ("ID", "Nombre", "Precio", "Categoría")
        self.tree_prod = ttk.Treeview(frame_tabla, columns=cols, show="headings")
        for col in cols:
            self.tree_prod.heading(col, text=col)
            self.tree_prod.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_prod.yview)
        self.tree_prod.configure(yscrollcommand=scrollbar.set)
        self.tree_prod.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

    def _construir_tab_usuarios(self):
        frame_form = ttk.LabelFrame(self.tab_usuarios, text="Registrar Usuario", padding=10)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frame_form, text="ID Usuario / Cédula:").pack(anchor="w")
        self.ent_u_id = ttk.Entry(frame_form)
        self.ent_u_id.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="Nombre Completo:").pack(anchor="w")
        self.ent_u_nombre = ttk.Entry(frame_form)
        self.ent_u_nombre.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="Correo Electrónico:").pack(anchor="w")
        self.ent_u_email = ttk.Entry(frame_form)
        self.ent_u_email.pack(fill="x", pady=(0, 15))

        btn_add_u = ttk.Button(frame_form, text="Guardar Usuario", command=self._guardar_usuario)
        btn_add_u.pack(fill="x", pady=2)

        frame_tabla = ttk.Frame(self.tab_usuarios, padding=10)
        frame_tabla.pack(side="right", expand=True, fill="both")

        cols = ("ID Usuario", "Nombre", "Correo")
        self.tree_user = ttk.Treeview(frame_tabla, columns=cols, show="headings")
        for col in cols:
            self.tree_user.heading(col, text=col)
            self.tree_user.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_user.yview)
        self.tree_user.configure(yscrollcommand=scrollbar.set)
        self.tree_user.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

    def _construir_tab_ventas(self):
        frame_form = ttk.LabelFrame(self.tab_ventas, text="Registrar Nueva Venta", padding=10)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frame_form, text="ID Usuario / Cliente:").pack(anchor="w")
        self.ent_v_usuario = ttk.Entry(frame_form)
        self.ent_v_usuario.insert(0, self.usuario_actual)
        self.ent_v_usuario.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="ID Producto:").pack(anchor="w")
        self.ent_v_producto = ttk.Entry(frame_form)
        self.ent_v_producto.pack(fill="x", pady=(0, 15))

        btn_venta = ttk.Button(frame_form, text="Procesar Venta", command=self._procesar_venta)
        btn_venta.pack(fill="x", pady=5)

        frame_tabla = ttk.Frame(self.tab_ventas, padding=10)
        frame_tabla.pack(side="right", expand=True, fill="both")

        cols = ("ID Venta", "Usuario", "Producto", "Total ($)", "Fecha")
        self.tree_ventas = ttk.Treeview(frame_tabla, columns=cols, show="headings")
        for col in cols:
            self.tree_ventas.heading(col, text=col)
            self.tree_ventas.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scrollbar.set)
        self.tree_ventas.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

    def _cargar_datos_tablas(self):
        for i in self.tree_prod.get_children():
            self.tree_prod.delete(i)
        for p in self.servicio.obtener_productos():
            p_id = getattr(p, "id", getattr(p, "id_producto", ""))
            cat = getattr(p, "categoria", "General")
            self.tree_prod.insert("", "end", values=(p_id, p.nombre, f"${p.precio:.2f}", cat))

        for i in self.tree_user.get_children():
            self.tree_user.delete(i)
        if hasattr(self.servicio, "obtener_usuarios"):
            for u in self.servicio.obtener_usuarios():
                u_id = getattr(u, "identificacion", getattr(u, "usuario", getattr(u, "id", "")))
                u_nom = getattr(u, "nombre", "")
                u_email = getattr(u, "correo", getattr(u, "email", ""))
                self.tree_user.insert("", "end", values=(u_id, u_nom, u_email))

        for i in self.tree_ventas.get_children():
            self.tree_ventas.delete(i)
        for v in self.servicio.obtener_ventas():
            self.tree_ventas.insert("", "end", values=(
                getattr(v, "id_venta", ""),
                getattr(v, "usuario_nombre", getattr(v, "usuario_id", "")),
                getattr(v, "producto_nombre", getattr(v, "producto_id", "")),
                f"${getattr(v, 'total', 0.0):.2f}",
                getattr(v, "fecha", "")
            ))

    def _guardar_producto(self):
        p_id = self.ent_p_id.get().strip()
        nom = self.ent_p_nombre.get().strip()
        prec = self.ent_p_precio.get().strip()
        cat = self.ent_p_cat.get().strip()

        exito, msj = self.servicio.registrar_producto(p_id, nom, prec, cat)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self._cargar_datos_tablas()
            self.ent_p_id.delete(0, tk.END)
            self.ent_p_nombre.delete(0, tk.END)
            self.ent_p_precio.delete(0, tk.END)
            self.ent_p_cat.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msj)

    def _eliminar_producto(self):
        sel = self.tree_prod.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto de la tabla para eliminar.")
            return

        item = self.tree_prod.item(sel[0])
        p_id = item["values"][0]

        exito, msj = self.servicio.eliminar_producto(str(p_id))
        if exito:
            messagebox.showinfo("Éxito", msj)
            self._cargar_datos_tablas()
        else:
            messagebox.showerror("Error", msj)

    def _guardar_usuario(self):
        u_id = self.ent_u_id.get().strip()
        nom = self.ent_u_nombre.get().strip()
        email = self.ent_u_email.get().strip()

        if hasattr(self.servicio, "registrar_usuario"):
            exito, msj = self.servicio.registrar_usuario(u_id, nom, email)
        else:
            exito, msj = False, "El servicio no tiene configurado el registro de usuarios."

        if exito:
            messagebox.showinfo("Éxito", msj)
            self._cargar_datos_tablas()
            self.ent_u_id.delete(0, tk.END)
            self.ent_u_nombre.delete(0, tk.END)
            self.ent_u_email.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msj)

    def _procesar_venta(self):
        u_id = self.ent_v_usuario.get().strip()
        p_id = self.ent_v_producto.get().strip()

        exito, msj = self.servicio.registrar_venta(u_id, p_id)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self._cargar_datos_tablas()
            self.ent_v_producto.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msj)

    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            if self.app_controller:
                self.app_controller.reiniciar_a_login()
            else:
                for widget in self.root.winfo_children():
                    widget.destroy()
                from ui.login_view import LoginView
                def on_success(usr):
                    for w in self.root.winfo_children():
                        w.destroy()
                    MainView(self.root, self.servicio, usr)
                LoginView(self.root, self.servicio, on_success).pack(expand=True, fill="both")