# Progress Training

API para la gestión de un centro de entrenamiento, construida con FastAPI y
SQLAlchemy.

## Estructura del proyecto
```text
proyecto-progress-training/
│
├── app/
│   ├── core/                  # Configuración global y dependencias
│   │   ├── __init__.py
│   │   ├── database.py        # Conexión SQLAlchemy con PostgreSQL
│   │   └── security.py        # Cifrado de contraseñas y autenticación por rol (RNF-03, RF-13)
│   │
│   ├── models/                # Modelos de SQLAlchemy (Mapeo de la Base de Datos - C4 Nivel 4)
│   │   ├── __init__.py
│   │   ├── usuario.py         # Clases Usuario, Empleado, Administrador
│   │   ├── cliente.py         # Entidad Cliente
│   │   ├── membresia.py       # Entidad Membresía
│   │   ├── pago.py            # Entidad Pago
│   │   ├── ingreso.py         # Entidad RegistroIngreso
│   │   ├── producto.py        # Entidad Producto y VentaProducto
│   │   ├── asistencia.py      # Entidad Asistencia
│   │   └── maquina.py         # Entidad Maquina y Mantenimiento
│   │
│   ├── schemas/               # Esquemas Pydantic (Validación de datos de entrada/salida HTTP)
│   │   ├── cliente_schema.py
│   │   ├── membresia_schema.py
│   │   ├── pago_schema.py
│   │   ├── ingreso_schema.py
│   │   ├── producto_schema.py
│   │   ├── asistencia_schema.py
│   │   └── maquina_schema.py
│   │
│   ├── repositories/          # Capa de Acceso a Datos (Repositorios - C4 Nivel 3)
│   │   ├── cliente_repository.py
│   │   ├── membresia_repository.py
│   │   ├── pago_repository.py
│   │   ├── usuario_repository.py
│   │   ├── ingreso_repository.py
│   │   ├── producto_repository.py
│   │   ├── asistencia_repository.py
│   │   └── maquina_repository.py
│   │
│   ├── patterns/              # Implementación de los 3 Patrones de Diseño GoF
│   │   ├── ingreso_facade.py  # Patrón Facade (Coordina el registro de ingreso - HU-02, HU-03)
│   │   ├── membresia_factory.py # Patrón Factory Method (Crea membresías por tipo - HU-04)
│   │   └── membresia_state.py # Patrón State (MembresiaVigente / MembresiaVencida - HU-03)
│   │
│   ├── routers/               # Endpoints de la API FastAPI (Controladores REST)
│   │   ├── auth.py            # Autenticación y roles (RF-13)
│   │   ├── clientes.py        # Gestión de clientes (HU-01)
│   │   ├── ingresos.py        # Control de ingresos (HU-02, HU-03)
│   │   ├── membresias.py      # Renovación y registro de membresías (HU-04)
│   │   ├── tienda.py          # Inventario y ventas de suplementos (HU-05)
│   │   ├── asistencia.py      # Control de asistencia de empleados (HU-06)
│   │   └── maquinas.py        # Gestión de estado de máquinas (HU-07)
│   │
│   └── main.py                # Punto de entrada de la aplicación FastAPI
│
├── requirements.txt           # Dependencias (FastAPI, SQLAlchemy, psycopg, pydantic)
└── README.md
```

### Carpetas y responsabilidades

- **`app/core/`**: configuración compartida de la aplicación. `database.py`
  centraliza la conexión a PostgreSQL y `security.py` contiene las utilidades
  de autenticación, autorización y seguridad.
- **`app/models/`**: modelos ORM de SQLAlchemy que representan las entidades
  del sistema, como usuarios, clientes, membresías, pagos, productos e
  ingresos.
- **`app/schemas/`**: esquemas Pydantic para validar y estructurar los datos
  que entran y salen de la API.
- **`app/repositories/`**: acceso a datos. Cada repositorio agrupa las
  operaciones de persistencia y consulta de una entidad, separándolas de los
  endpoints y de las reglas de negocio.
- **`app/patterns/`**: patrones de diseño del dominio. La fachada coordina el
  registro de ingresos; la fábrica crea membresías según su tipo; y el patrón
  State representa los distintos estados de una membresía.
- **`app/routers/`**: endpoints HTTP de FastAPI organizados por funcionalidad,
  como clientes, membresías, ingresos, tienda, asistencia y máquinas.

### Archivos principales

- **`app/main.py`**: crea la aplicación FastAPI y sirve como punto de entrada.
  Aquí se conectan los routers para exponer sus endpoints.
- **`requirements.txt`**: lista las dependencias de Python necesarias para
  instalar y ejecutar el proyecto.
- **`README.md`**: contiene la descripción, estructura e instrucciones de uso
  del proyecto.

### Flujo general de una solicitud

Una solicitud llega a un router, donde se valida su entrada con los esquemas
Pydantic. El router delega la operación a la lógica correspondiente y a los
patrones de dominio cuando aplica; el repositorio consulta o modifica los
modelos persistidos en la base de datos. Finalmente, la API devuelve una
respuesta validada y serializada mediante los esquemas.

## Preparación

1. Crea y activa un entorno virtual de Python.
2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la raíz y configura `DATABASE_URL` con la URL de
   conexión de Neon (PostgreSQL), por ejemplo:

   ```env
   DATABASE_URL=postgresql+psycopg://usuario:contraseña@servidor.neon.tech/base_de_datos?sslmode=require
   ```

   Si el usuario o la contraseña contienen caracteres especiales, deben estar
   codificados para URL.

4. Inicia el servidor de desarrollo desde la raíz del proyecto:

   ```bash
   uvicorn app.main:app --reload
   ```

La documentación interactiva de la API estará disponible en `/docs`.

El backend permite solicitudes desde `http://localhost:4200` y
`http://127.0.0.1:4200` mediante CORS para el desarrollo local, también cuando
la aplicación devuelve un error interno. Reinicia Uvicorn después de modificar
la configuración de la aplicación.
### Control de asistencia

- `POST /asistencias` registra una `Entrada` o una `Salida` para un empleado.
  La salida completa la entrada pendiente más reciente; si no existe, la API
  responde `409 Conflict`.
- `GET /asistencias/empleado/{empleado_id}` consulta el historial del empleado.

La respuesta contiene `fecha_entrada` y `fecha_salida`; al registrar una
entrada, `fecha_salida` queda vacía hasta marcar la salida.

La conexión a PostgreSQL se configura en `app/core/database.py`. Los
repositorios pueden recibir sesiones con la dependencia `get_db`; la creación
de tablas se hace al arrancar con `Base.metadata.create_all()` (en `main.py`).
Ojo: `create_all()` no modifica tablas que ya existen; los cambios de columnas
se aplican a mano en el SQL Editor de Neon.
