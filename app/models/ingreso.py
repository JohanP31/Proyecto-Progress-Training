from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class RegistroIngresoModel(Base):
    __tablename__ = "registros_ingreso"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, nullable=False)
    tipo_ingreso = Column(String(50), nullable=False)

    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    # Empleado que registró el ingreso
    # (lo recibe IngresoFacade.registrarIngreso)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=False)

    cliente = relationship("ClienteModel", back_populates="ingresos")
    empleado = relationship("EmpleadoModel")
