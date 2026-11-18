"""Acceso a datos de registros de ingreso."""

from sqlalchemy.orm import Session

from app.models.ingreso import RegistroIngresoModel


class IngresoRepository:
    """Guarda registros de ingreso. Es lo único que habla con la tabla."""

    def __init__(self, db: Session):
        # Sesión de base de datos que recibe desde afuera
        self.db = db

    def guardar(self, registro: RegistroIngresoModel) -> RegistroIngresoModel:
        """Guarda un registro de ingreso y lo devuelve con su id."""
        self.db.add(registro)
        self.db.commit()
        self.db.refresh(registro)
        return registro
