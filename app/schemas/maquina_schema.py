"""Esquemas de entrada y salida para máquinas."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MaquinaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    estado: Literal["Disponible", "En mantenimiento", "Dañada"] = "Disponible"
    fecha_adquisicion: date | None = None

    @field_validator("nombre", "estado", mode="before")
    @classmethod
    def limpiar_textos(cls, value: str) -> str:
        if isinstance(value, str):
            return " ".join(value.strip().split())
        return value


class MantenimientoResponse(BaseModel):
    id: int
    fecha: date
    descripcion: str
    costo: float
    estado: str
    maquina_id: int

    model_config = ConfigDict(from_attributes=True)


class MantenimientoCreate(BaseModel):
    fecha: date
    descripcion: str = Field(min_length=1, max_length=255)
    costo: float = Field(ge=0)
    estado: str = Field(min_length=1, max_length=50)

    @field_validator("descripcion", "estado", mode="before")
    @classmethod
    def limpiar_textos(cls, value: str) -> str:
        if isinstance(value, str):
            return " ".join(value.strip().split())
        return value


class MaquinaResponse(BaseModel):
    id: int
    nombre: str
    estado: str
    fecha_adquisicion: date | None = None
    mantenimientos: list[MantenimientoResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
