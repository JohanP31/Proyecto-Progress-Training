"""Esquemas de entrada y salida para clientes."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ClienteCrear(BaseModel):
    """Datos que se piden para registrar un cliente (HU-01)."""

    # Los límites coinciden con el tamaño de las columnas en la base de datos
    nombre: str = Field(min_length=1, max_length=100)
    documento: str = Field(min_length=1, max_length=50)
    telefono: str | None = Field(default=None, max_length=20)
    fecha_nacimiento: date | None = None


class ClienteRespuesta(BaseModel):
    """Datos del cliente que devuelve la API."""

    # Permite crear esta respuesta directamente desde ClienteModel
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    documento: str
    telefono: str | None
    fecha_nacimiento: date | None
    estado: str
