"""Endpoints para el control de ingresos (HU-02 y HU-03)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.patterns.ingreso_facade import (
    ClienteNoEncontradoError,
    EmpleadoNoEncontradoError,
    IngresoBloqueadoError,
    IngresoFacade,
)
from app.schemas.ingreso_schema import IngresoCrear, IngresoRespuesta

router = APIRouter(prefix="/ingresos", tags=["ingresos"])


@router.post(
    "",
    response_model=IngresoRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def registrar_ingreso(datos: IngresoCrear, db: Session = Depends(get_db)):
    """HU-02 y HU-03: registra el ingreso si la membresía está vigente."""
    try:
        return IngresoFacade(db).registrarIngreso(
            datos.cliente_id, datos.empleado_id
        )
    # Convierte los errores de la Facade en respuestas HTTP
    except ClienteNoEncontradoError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )
    except EmpleadoNoEncontradoError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado.",
        )
    except IngresoBloqueadoError as error:
        # HU-03: ingreso bloqueado (no se guarda nada)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Ingreso bloqueado. {error}",
        )
