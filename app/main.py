"""Punto de entrada de la API FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401  (registra todos los modelos)
from app.core.database import Base, engine
from app.routers import asistencia, clientes, ingresos, maquinas, membresias, tienda

# Crea en la base de datos las tablas que todavía no existen.
# Ojo: no modifica tablas que ya existen.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Progress Training API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers del MVP
app.include_router(clientes.router)
app.include_router(ingresos.router)
app.include_router(maquinas.router)
app.include_router(membresias.router)
app.include_router(tienda.router)
app.include_router(asistencia.router)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    """Confirma que la API está disponible."""
    return {"status": "ok"}
