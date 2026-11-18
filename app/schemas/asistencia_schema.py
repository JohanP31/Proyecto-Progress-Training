"""Esquemas de entrada y salida para asistencias."""

from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class AsistenciaCreate(BaseModel):
    empleado_id: int = Field(gt=0)
    tipo_registro: Literal["Entrada", "Salida"] = "Entrada"

    @field_validator("tipo_registro", mode="before")
    @classmethod
    def limpiar_tipo(cls, value: Any) -> Any:
        if isinstance(value, str):
            return " ".join(value.strip().split())
        return value


class AsistenciaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_entrada: datetime | None
    fecha_salida: datetime | None
    empleado_id: int
