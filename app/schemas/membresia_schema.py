"""Esquemas de entrada y salida para membresías."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.pago_schema import PagoRespuesta


class RenovacionCrear(BaseModel):
    """Datos que se piden para renovar una membresía (HU-04)."""

    cliente_id: int = Field(gt=0)
    # Tipos que sabe crear MembresiaFactory
    tipo: Literal["mensualidad", "ingreso_unico"]
    metodo_pago: str = Field(min_length=1, max_length=50)


class MembresiaRespuesta(BaseModel):
    """Datos de la membresía que devuelve la API."""

    # Permite crear esta respuesta directamente desde MembresiaModel
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: str
    fecha_inicio: date
    fecha_fin: date
    valor: float
    cliente_id: int
    # "Vigente" o "Vencida": lo calcula el patrón State
    nombre_estado: str


class RenovacionRespuesta(BaseModel):
    """Resultado de renovar: la membresía nueva y su pago."""

    membresia: MembresiaRespuesta
    pago: PagoRespuesta
