from datetime import datetime
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self):
        self.archivo_servicio = ArchivoServicio()
        self.productos = []
        self.usuarios = []
        self.ventas = []
        self._cargar_datos()

    def _cargar_datos(self):
        # Cargar productos
        prods_dict = self.archivo_servicio.cargar_productos()
        self.productos = []
        for p in prods_dict:
            p_id = p.get("id") or p.get("id_producto") or ""
            p_nom = p.get("nombre", "")
            p_prec = p.get("precio", 0.0)
            p_cat = p.get("categoria", "General")
            self.productos.append(Producto(p_id, p_nom, p_prec, p_cat))

        # Cargar usuarios
        usua_dict = self.archivo_servicio.cargar_usuarios()
        self.usuarios = []
        for u in usua_dict:
            u_id = u.get("identificacion") or u.get("usuario") or u.get("id") or ""
            u_nom = u.get("nombre") or u.get("usuario") or ""
            u_cor = u.get("correo") or u.get("email") or ""
            u_clave = u.get("clave") or u.get("password") or u.get("contrasena") or ""
            
            usr_obj = Usuario(u_id, u_nom, u_cor)
            usr_obj.clave = u_clave
            self.usuarios.append(usr_obj)

        # Cargar ventas
        ventas_dict = self.archivo_servicio.cargar_ventas()
        self.ventas = []
        for v in ventas_dict:
            self.ventas.append(Venta(
                v.get("id_venta", ""),
                v.get("usuario_id", ""),
                v.get("usuario_nombre", ""),
                v.get("producto_id", ""),
                v.get("producto_nombre", ""),
                v.get("total", 0.0),
                v.get("fecha", "")
            ))

    def validar_acceso(self, usuario, clave):
        if not usuario or not clave:
            return False

        if usuario.strip().lower() == "admin" and clave.strip() in ["123", "admin", "1234"]:
            return True

        for u in self.usuarios:
            id_u = getattr(u, "identificacion", getattr(u, "usuario", ""))
            clave_u = getattr(u, "clave", getattr(u, "password", ""))
            
            if str(id_u).strip().lower() == str(usuario).strip().lower():
                if not clave_u or str(clave_u).strip() == str(clave).strip():
                    return True

        return False

    def _obtener_id_producto(self, producto):
        return getattr(producto, "id", getattr(producto, "id_producto", ""))

    def obtener_productos(self):
        return self.productos

    def obtener_usuarios(self):
        return self.usuarios

    def obtener_ventas(self):
        return self.ventas

    def buscar_producto_por_id(self, id_prod):
        for p in self.productos:
            if self._obtener_id_producto(p) == id_prod:
                return p
        return None

    def buscar_usuario_por_id(self, id_usu):
        for u in self.usuarios:
            id_u = getattr(u, "identificacion", getattr(u, "usuario", ""))
            if str(id_u).strip().lower() == str(id_usu).strip().lower():
                return u
        return None

    def registrar_producto(self, id_prod, nombre, precio, categoria):
        if not id_prod or not nombre or not precio:
            return False, "Todos los campos obligatorios deben ser completados."
        if self.buscar_producto_por_id(id_prod):
            return False, f"Ya existe un producto con el ID '{id_prod}'."
        try:
            precio_val = float(precio)
        except ValueError:
            return False, "El precio debe ser un número válido."

        nuevo_p = Producto(id_prod, nombre, precio_val, categoria if categoria else "General")
        self.productos.append(nuevo_p)
        self.archivo_servicio.guardar_productos([p.to_dict() for p in self.productos])
        return True, f"Producto '{nombre}' registrado con éxito."

    def registrar_usuario(self, id_usu, nombre, correo, clave="123"):
        if not id_usu or not nombre:
            return False, "El ID y el Nombre son obligatorios."
        if self.buscar_usuario_por_id(id_usu):
            return False, f"Ya existe un usuario con el ID '{id_usu}'."

        nuevo_u = Usuario(id_usu, nombre, correo)
        nuevo_u.clave = clave
        self.usuarios.append(nuevo_u)
        self.archivo_servicio.guardar_usuarios([u.to_dict() for u in self.usuarios])
        return True, f"Usuario '{nombre}' registrado con éxito."

    def eliminar_producto(self, id_prod):
        prod = self.buscar_producto_por_id(id_prod)
        if not prod:
            return False, f"No se encontró el producto con ID '{id_prod}'."
        self.productos.remove(prod)
        self.archivo_servicio.guardar_productos([p.to_dict() for p in self.productos])
        return True, f"Producto '{id_prod}' eliminado correctamente."

    def registrar_venta(self, usuario_id, producto_id):
        usuario = self.buscar_usuario_por_id(usuario_id)
        producto = self.buscar_producto_por_id(producto_id)

        if not usuario and usuario_id.lower() != "admin":
            return False, "El usuario seleccionado no existe."
        if not producto:
            return False, "El producto seleccionado no existe."

        id_venta = f"V{len(self.ventas) + 1:03d}"
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if usuario:
            u_id = getattr(usuario, "identificacion", getattr(usuario, "usuario", usuario_id))
            u_nom = getattr(usuario, "nombre", u_id)
        else:
            u_id = "admin"
            u_nom = "Administrador"

        nueva_venta = Venta(
            id_venta=id_venta,
            usuario_id=u_id,
            usuario_nombre=u_nom,
            producto_id=self._obtener_id_producto(producto),
            producto_nombre=producto.nombre,
            total=producto.precio,
            fecha=fecha_actual
        )

        self.ventas.append(nueva_venta)
        self.archivo_servicio.guardar_ventas([v.to_dict() for v in self.ventas])
        return True, f"Venta {id_venta} registrada exitosamente por ${producto.precio:.2f}."