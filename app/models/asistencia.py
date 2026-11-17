from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class AsistenciaModel(Base):
    __tablename__ = "asistencias"

    id = Column(Integer, primary_key=True, index=True)
    fecha_entrada = Column(DateTime, nullable=True)
    fecha_salida = Column(DateTime, nullable=True)

    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=False)

    empleado = relationship("EmpleadoModel", back_populates="asistencias")
