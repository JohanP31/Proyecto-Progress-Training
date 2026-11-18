"""Endpoints para el control de asistencia de empleados."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.asistencia_repository import (
    AsistenciaRepository,
    NoHayEntradaAbiertaError,
)
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.asistencia_schema import AsistenciaCreate, AsistenciaResponse

router = APIRouter(prefix="/asistencias", tags=["asistencias"])


@router.post(
    "",
    response_model=AsistenciaResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_asistencia(
    datos: AsistenciaCreate, db: Session = Depends(get_db)
):
    """Registra la entrada o salida de un empleado."""
    if not UsuarioRepository.existe_empleado(db, datos.empleado_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado.",
        )

    try:
        return AsistenciaRepository.registrar_asistencia(
            db, datos.empleado_id, datos.tipo_registro
        )
    except NoHayEntradaAbiertaError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No hay una entrada pendiente para registrar la salida.",
        ) from None


@router.get(
    "/empleado/{empleado_id}",
    response_model=list[AsistenciaResponse],
)
def listar_asistencias_por_empleado(
    empleado_id: int, db: Session = Depends(get_db)
):
    """Consulta el historial de asistencias de un empleado específico."""
    if not UsuarioRepository.existe_empleado(db, empleado_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado.",
        )

    return AsistenciaRepository.obtener_por_empleado(db, empleado_id)
