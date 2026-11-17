"""Endpoints para inventario y venta de productos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.producto_schema import (
    ProductoCreate,
    ProductoResponse,
    VentaProductoCreate,
    VentaProductoResult,
)
from app.repositories.producto_repository import ProductoRepository

router = APIRouter(prefix="/productos", tags=["Tienda y Productos"])


@router.get("/", response_model=List[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return ProductoRepository.obtener_todos(db)


@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    return ProductoRepository.crear(db, datos)


@router.post("/ventas", response_model=VentaProductoResult, status_code=201)
def realizar_venta(datos: VentaProductoCreate, db: Session = Depends(get_db)):
    producto = ProductoRepository.obtener_por_id(db, datos.producto_id)
    if not producto:
        raise HTTPException(
            status_code=404, detail="Producto no encontrado en el inventario."
        )

    if producto.stock < datos.cantidad:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente. Stock actual disponible: {producto.stock}",
        )

    venta = ProductoRepository.registrar_venta(db, producto, datos)
    return {
        "mensaje": "Venta registrada con éxito",
        "venta_id": venta.id,
        "producto": producto.nombre,
        "cantidad_vendida": venta.cantidad,
        "total_pagado": venta.total,
        "stock_restante": producto.stock,
    }
