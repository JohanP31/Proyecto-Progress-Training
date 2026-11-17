from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProductoModel(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    precio_unitario = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    ventas = relationship("VentaProductoModel", back_populates="producto")


class VentaProductoModel(Base):
    __tablename__ = "ventas_productos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False)
    cantidad = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)

    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)

    producto = relationship("ProductoModel", back_populates="ventas")
