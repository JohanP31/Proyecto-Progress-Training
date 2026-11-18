"""Acceso a datos de membresías."""

from sqlalchemy.orm import Session

from app.models.membresia import MembresiaModel


class MembresiaRepository:
    """Guarda y busca membresías. Es lo único que habla con la tabla."""

    def __init__(self, db: Session):
        # Sesión de base de datos que recibe desde afuera
        self.db = db

    def crear(self, membresia: MembresiaModel) -> MembresiaModel:
        """Guarda una membresía nueva y la devuelve con su id."""
        self.db.add(membresia)
        self.db.commit()
        self.db.refresh(membresia)
        return membresia

    def buscar_ultima(self, cliente_id: int) -> MembresiaModel | None:
        """Devuelve la membresía del cliente que termina más tarde."""
        return (
            self.db.query(MembresiaModel)
            .filter(MembresiaModel.cliente_id == cliente_id)
            .order_by(MembresiaModel.fecha_fin.desc())
            .first()
        )
