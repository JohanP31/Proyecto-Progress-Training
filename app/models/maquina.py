from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class MaquinaModel(Base):
    __tablename__ = "maquinas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(String(50), nullable=False)
    fecha_adquisicion = Column(Date, nullable=True)

    mantenimientos = relationship(
        "MantenimientoModel",
        back_populates="maquina",
        cascade="all, delete-orphan",
    )


class MantenimientoModel(Base):
    __tablename__ = "mantenimientos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String(255), nullable=False)
    costo = Column(Float, nullable=False)
    estado = Column(String(50), nullable=False)

    maquina_id = Column(Integer, ForeignKey("maquinas.id"), nullable=False)

    maquina = relationship("MaquinaModel", back_populates="mantenimientos")
