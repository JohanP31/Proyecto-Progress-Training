"""Esquemas de entrada y salida para pagos."""

from datetime import date

from pydantic import BaseModel, ConfigDict


class PagoRespuesta(BaseModel):
    """Datos del pago que devuelve la API."""

    # Permite crear esta respuesta directamente desde PagoModel
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: date
    monto: float
    metodo_pago: str
    concepto: str
    membresia_id: int
