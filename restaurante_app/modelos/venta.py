class Venta:
    def __init__(self, id_venta, usuario_id, usuario_nombre, producto_id, producto_nombre, total, fecha):
        self.id_venta = id_venta
        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.total = float(total) if total is not None else 0.0
        self.fecha = fecha

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "usuario_id": self.usuario_id,
            "usuario_nombre": self.usuario_nombre,
            "producto_id": self.producto_id,
            "producto_nombre": self.producto_nombre,
            "total": self.total,
            "fecha": self.fecha
        }