"""Acceso a datos de usuarios (empleados y administradores)."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.usuario import EmpleadoModel, UsuarioModel


class UsuarioDuplicadoError(Exception):
    """Se lanza cuando el correo o documento ya está registrado."""


class UsuarioRepository:
    """Guarda y busca usuarios, empleados y administradores."""

    @staticmethod
    def crear_usuario(db: Session, usuario: UsuarioModel) -> UsuarioModel:
        """Guarda un usuario nuevo y lo devuelve con su id."""
        db.add(usuario)
        try:
            db.commit()
        except IntegrityError as error:
            db.rollback()
            raise UsuarioDuplicadoError from error
        db.refresh(usuario)
        return usuario

    @staticmethod
    def obtener_por_id(db: Session, usuario_id: int) -> UsuarioModel | None:
        return db.get(UsuarioModel, usuario_id)

    @staticmethod
    def obtener_por_correo(db: Session, correo: str) -> UsuarioModel | None:
        return (
            db.query(UsuarioModel)
            .filter(UsuarioModel.correo == correo)
            .first()
        )

    @staticmethod
    def obtener_por_documento(
        db: Session, documento: str
    ) -> UsuarioModel | None:
        return (
            db.query(UsuarioModel)
            .filter(UsuarioModel.documento == documento)
            .first()
        )

    @staticmethod
    def listar_empleados(db: Session) -> list[UsuarioModel]:
        """Devuelve todos los usuarios que pertenecen al subtipo empleado."""
        return (
            db.query(UsuarioModel)
            .filter(
                UsuarioModel.rol
                == EmpleadoModel.__mapper__.polymorphic_identity
            )
            .all()
        )

    @staticmethod
    def existe_empleado(db: Session, empleado_id: int) -> bool:
        return (
            db.query(EmpleadoModel.id)
            .filter(EmpleadoModel.id == empleado_id)
            .first()
            is not None
        )
