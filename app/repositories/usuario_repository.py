"""Acceso a datos de usuarios (empleados y administradores)."""

from sqlalchemy.orm import Session
from app.models.usuario import EmpleadoModel, UsuarioModel


class UsuarioRepository:
    """Busca usuarios y empleados."""

    @staticmethod
    def obtener_por_id(db: Session, usuario_id: int) -> UsuarioModel | None:
        return db.get(UsuarioModel, usuario_id)

    @staticmethod
    def obtener_por_correo(db: Session, correo: str) -> UsuarioModel | None:
        return db.query(UsuarioModel).filter(UsuarioModel.correo == correo).first()

    @staticmethod
    def existe_empleado(db: Session, empleado_id: int) -> bool:
        return (
            db.query(EmpleadoModel.id)
            .filter(EmpleadoModel.id == empleado_id)
            .first()
            is not None
        )
