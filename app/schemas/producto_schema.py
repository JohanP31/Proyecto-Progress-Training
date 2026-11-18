"""Esquemas de entrada y salida para productos."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    categoria: str = Field(min_length=1, max_length=50)
    precio_unitario: float = Field(gt=0)
    stock: int = Field(ge=0)

    @field_validator("nombre", "categoria", mode="before")
    @classmethod
    def limpiar_textos(cls, value: str) -> str:
        if isinstance(value, str):
            return " ".join(value.strip().split())
        return value


class VentaProductoResponse(BaseModel):
    id: int
    fecha: datetime
    cantidad: int
    total: float
    producto_id: int

    model_config = ConfigDict(from_attributes=True)


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    categoria: str
    precio_unitario: float
    stock: int
    ventas: list[VentaProductoResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class VentaProductoCreate(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0)


class VentaProductoResult(BaseModel):
    mensaje: str
    venta_id: int
    producto: str
    cantidad_vendida: int
    total_pagado: float
    stock_restante: int
