"""Esquemas de entrada y salida para registros de ingreso."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class IngresoCrear(BaseModel):
    """Datos que se piden para registrar un ingreso (HU-02)."""

    cliente_id: int = Field(gt=0)
    # Empleado que está en recepción registrando el ingreso
    empleado_id: int = Field(gt=0)


class IngresoRespuesta(BaseModel):
    """Datos del ingreso que devuelve la API."""

    # Permite crear esta respuesta directamente desde RegistroIngresoModel
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_hora: datetime
    # Tipo de membresía con la que entró el cliente
    tipo_ingreso: str
    cliente_id: int
    empleado_id: int
