"""Endpoints para la gestión del estado de las máquinas."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.maquina_schema import (
    MaquinaCreate,
    MaquinaResponse,
    MantenimientoCreate,
    MantenimientoResponse,
)
from app.repositories.maquina_repository import MaquinaRepository

router = APIRouter(prefix="/maquinas", tags=["Máquinas y Mantenimiento"])


@router.get("/", response_model=List[MaquinaResponse])
def listar_maquinas(db: Session = Depends(get_db)):
    return MaquinaRepository.obtener_todas(db)


@router.post("/", response_model=MaquinaResponse, status_code=201)
def crear_maquina(datos: MaquinaCreate, db: Session = Depends(get_db)):
    return MaquinaRepository.crear(db, datos)


@router.post(
    "/{maquina_id}/mantenimientos",
    response_model=MantenimientoResponse,
    status_code=201,
)
def registrar_mantenimiento(
    maquina_id: int, datos: MantenimientoCreate, db: Session = Depends(get_db)
):
    maquina = MaquinaRepository.obtener_por_id(db, maquina_id)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada.")

    return MaquinaRepository.registrar_mantenimiento(db, maquina, datos)


@router.put("/{maquina_id}/estado", response_model=MaquinaResponse)
def actualizar_estado_maquina(
    maquina_id: int, nuevo_estado: str, db: Session = Depends(get_db)
):
    maquina = MaquinaRepository.obtener_por_id(db, maquina_id)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada.")

    estados_validos = ["Disponible", "En mantenimiento", "Dañada"]
    if nuevo_estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido. Debe ser uno de: {estados_validos}",
        )

    return MaquinaRepository.actualizar_estado(db, maquina, nuevo_estado)
