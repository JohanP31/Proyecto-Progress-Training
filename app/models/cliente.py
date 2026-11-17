from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    documento = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    estado = Column(String(20), default="Activo")

    membresias = relationship(
        "MembresiaModel",
        back_populates="cliente",
        cascade="all, delete-orphan",
    )
    ingresos = relationship(
        "RegistroIngresoModel",
        back_populates="cliente",
        cascade="all, delete-orphan",
    )
