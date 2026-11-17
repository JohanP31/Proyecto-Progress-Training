"""Acceso a datos de productos y ventas."""

from sqlalchemy.orm import Session, selectinload
from app.models.producto import ProductoModel, VentaProductoModel
from app.schemas.producto_schema import ProductoCreate, VentaProductoCreate
from datetime import datetime


class ProductoRepository:

    @staticmethod
    def obtener_todos(db: Session):
        return (
            db.query(ProductoModel)
            .options(selectinload(ProductoModel.ventas))
            .all()
        )

    @staticmethod
    def obtener_por_id(db: Session, producto_id: int):
        return db.query(ProductoModel).filter(ProductoModel.id == producto_id).first()

    @staticmethod
    def crear(db: Session, datos: ProductoCreate):
        db_producto = ProductoModel(
            nombre=datos.nombre,
            categoria=datos.categoria,
            precio_unitario=datos.precio_unitario,
            stock=datos.stock,
        )
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto

    @staticmethod
    def registrar_venta(
        db: Session, producto: ProductoModel, datos: VentaProductoCreate
    ):
        cantidad = datos.cantidad
        total_venta = producto.precio_unitario * cantidad

        # Descontar stock
        producto.stock -= cantidad

        # Crear registro de venta
        db_venta = VentaProductoModel(
            fecha=datetime.now(),
            cantidad=cantidad,
            total=total_venta,
            producto=producto,
        )
        db.add(db_venta)
        db.commit()
        db.refresh(db_venta)
        return db_venta
