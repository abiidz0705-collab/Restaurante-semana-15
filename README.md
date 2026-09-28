# Restaurante App - Semana 15: Componentes y Contenedores

**Estudiante:** Abigail Deleg
**Asignatura:** Programación Orientada a Objetos  
**Semana:** 15

## Descripción del Proyecto
Evolución de la aplicación **Restaurante App** integrando el concepto fundamental de **Manejo de Eventos** en Tkinter. Se incorpora el módulo de **Ventas**, permitiendo que las acciones del usuario activen botones mediante `command=`, ejecuten **callbacks** de respuesta, deleguen la validación a `RestauranteServicio` y mantengan la persistencia en `ventas.json`.

---

##  Flujo de Manejo de Eventos
[ USUARIO ]
│ (Acción: Seleccionar datos y presionar botón)
▼
[ BOTÓN: "Registrar Venta" ] ── (command=) ──► [ CALLBACK: _callback_registrar_venta ]
│
▼
[ RestauranteServicio ]
│
▼
[ datos/ventas.json ]
│
▼
[ Actualización Treeview ]

---

## Estructura del Proyecto
restaurante_app/
├── assets/                  # Recursos gráficos (íconos, logotipos)
├── datos/
│   ├── productos.json       # Persistencia de productos
│   ├── usuarios.json        # Persistencia de usuarios
│   └── ventas.json          # Persistencia de ventas
├── modelos/
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py             # Modelo de la entidad Venta
├── servicios/
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py # Lógica de negocio y persistencia
├── ui/
│   ├── login_view.py
│   └── main_view.py         # Formulario y tabla de ventas con eventos
├── main.py                  # Punto de entrada
└── README.md

---

## Instrucciones de Ejecución
```bash
python main.py
(O python restaurante_app/main.py desde el directorio superior).
