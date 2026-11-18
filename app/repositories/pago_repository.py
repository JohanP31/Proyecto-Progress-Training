"""Acceso a datos de pagos."""

from sqlalchemy.orm import Session

from app.models.pago import PagoModel


class PagoRepository:
    """Guarda pagos. Es lo único que habla con la tabla de pagos."""

    def __init__(self, db: Session):
        # Sesión de base de datos que recibe desde afuera
        self.db = db

    def crear(self, pago: PagoModel) -> PagoModel:
        """Guarda un pago nuevo y lo devuelve con su id."""
        self.db.add(pago)
        self.db.commit()
        self.db.refresh(pago)
        return pago
