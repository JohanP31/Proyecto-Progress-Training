"""Esquemas de entrada y salida para usuarios (empleados y administradores)."""

from typing import Any, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


class UsuarioCreate(BaseModel):
    """Datos para registrar un usuario interno.

    Administrador: lleva nivel_acceso y NO lleva cargo ni salario.
    Empleado: lleva cargo y salario y NO lleva nivel_acceso.
    """

    # Ejemplos que se ven en Swagger (/docs)
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "nombre": "Ana Pérez",
                    "documento": "1000000001",
                    "telefono": "3000000001",
                    "correo": "admin@example.com",
                    "contrasena": "clave-de-prueba",
                    "rol": "Administrador",
                    "nivel_acceso": "TOTAL",
                },
                {
                    "nombre": "Luis Gómez",
                    "documento": "987654321",
                    "telefono": "3107654321",
                    "correo": "luis@example.com",
                    "contrasena": "clave-de-prueba",
                    "rol": "Empleado",
                    "cargo": "Entrenador",
                    "salario": 2500000,
                },
            ]
        }
    )

    nombre: str = Field(min_length=1, max_length=100)
    documento: str = Field(min_length=1, max_length=50)
    telefono: str | None = Field(default=None, max_length=20)
    correo: EmailStr = Field(max_length=100)
    contrasena: str = Field(min_length=1, max_length=255)
    rol: Literal["Administrador", "Empleado"]

    nivel_acceso: str | None = Field(default=None, min_length=1, max_length=50)
    cargo: str | None = Field(default=None, min_length=1, max_length=50)
    salario: float | None = None

    @field_validator("nombre", mode="before")
    @classmethod
    def limpiar_nombre(cls, valor: Any) -> Any:
        if not isinstance(valor, str):
            return valor
        return " ".join(valor.strip().split())

    @field_validator("correo", mode="before")
    @classmethod
    def limpiar_correo(cls, valor: Any) -> Any:
        if not isinstance(valor, str):
            return valor
        return valor.strip().lower()

    @field_validator("documento", mode="before")
    @classmethod
    def limpiar_documento(cls, valor: Any) -> Any:
        if not isinstance(valor, str):
            return valor
        return valor.strip()

    @model_validator(mode="after")
    def validar_campos_por_rol(self) -> Self:
        if self.rol == "Administrador":
            if self.nivel_acceso is None:
                raise ValueError(
                    "nivel_acceso es obligatorio para Administrador."
                )
            if self.cargo is not None or self.salario is not None:
                raise ValueError(
                    "cargo y salario solo corresponden a Empleado."
                )
        else:
            if self.cargo is None or self.salario is None:
                raise ValueError(
                    "cargo y salario son obligatorios para Empleado."
                )
            if self.nivel_acceso is not None:
                raise ValueError(
                    "nivel_acceso solo corresponde a Administrador."
                )
        return self


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    documento: str
    telefono: str | None
    correo: str
    rol: str
    nivel_acceso: str | None = None
    cargo: str | None = None
    salario: float | None = None
