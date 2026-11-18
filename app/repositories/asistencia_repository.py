"""Acceso a datos de asistencias."""

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.asistencia import AsistenciaModel


class AsistenciaRepository:
    """Registra y consulta los marcajes de asistencia."""

    @staticmethod
    def registrar_asistencia(
        db: Session, empleado_id: int, tipo_registro: str
    ) -> AsistenciaModel:
        if tipo_registro == "Entrada":
            asistencia = AsistenciaModel(
                fecha_entrada=datetime.now(),
                empleado_id=empleado_id,
            )
            db.add(asistencia)
        else:
            asistencia = (
                db.query(AsistenciaModel)
                .filter(
                    AsistenciaModel.empleado_id == empleado_id,
                    AsistenciaModel.fecha_entrada.is_not(None),
                    AsistenciaModel.fecha_salida.is_(None),
                )
                .order_by(AsistenciaModel.fecha_entrada.desc())
                .first()
            )
            if asistencia is None:
                raise NoHayEntradaAbiertaError(empleado_id)
            asistencia.fecha_salida = datetime.now()

        db.commit()
        db.refresh(asistencia)
        return asistencia

    @staticmethod
    def obtener_por_empleado(db: Session, empleado_id: int) -> list[AsistenciaModel]:
        return (
            db.query(AsistenciaModel)
            .filter(AsistenciaModel.empleado_id == empleado_id)
            .order_by(AsistenciaModel.fecha_entrada.desc())
            .all()
        )


class NoHayEntradaAbiertaError(Exception):
    """Se intenta registrar una salida sin una entrada pendiente."""
