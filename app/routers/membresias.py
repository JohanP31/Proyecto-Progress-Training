"""Endpoints para el registro y renovación de membresías (HU-04)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.membresia_schema import (
    MembresiaRespuesta,
    RenovacionCrear,
    RenovacionRespuesta,
)
from app.services.membresia_service import (
    ClienteNoEncontradoError,
    MembresiaService,
)

router = APIRouter(prefix="/membresias", tags=["membresias"])


@router.post(
    "/renovar",
    response_model=RenovacionRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def renovar_membresia(datos: RenovacionCrear, db: Session = Depends(get_db)):
    """HU-04: renueva la membresía de un cliente y registra el pago."""
    try:
        membresia, pago = MembresiaService(db).renovar(
            datos.cliente_id, datos.tipo, datos.metodo_pago
        )
    except ClienteNoEncontradoError:
        # Convierte el error del servicio en una respuesta HTTP
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )
    return {"membresia": membresia, "pago": pago}


@router.get(
    "/cliente/{cliente_id}",
    response_model=MembresiaRespuesta,
)
def consultar_membresia(cliente_id: int, db: Session = Depends(get_db)):
    """Consulta la membresía más reciente de un cliente y su estado."""
    try:
        membresia = MembresiaService(db).consultar_actual(cliente_id)
    except ClienteNoEncontradoError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )
    if membresia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente no tiene membresías.",
        )
    return membresia
