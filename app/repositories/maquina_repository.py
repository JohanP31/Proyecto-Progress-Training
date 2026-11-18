"""Acceso a datos de máquinas y mantenimientos."""

from sqlalchemy.orm import Session, selectinload
from app.models.maquina import MaquinaModel, MantenimientoModel
from app.schemas.maquina_schema import MaquinaCreate, MantenimientoCreate


class MaquinaRepository:

    @staticmethod
    def obtener_todas(db: Session):
        return (
            db.query(MaquinaModel)
            .options(selectinload(MaquinaModel.mantenimientos))
            .all()
        )

    @staticmethod
    def obtener_por_id(db: Session, maquina_id: int):
        return (
            db.query(MaquinaModel)
            .filter(MaquinaModel.id == maquina_id)
            .first()
        )

    @staticmethod
    def crear(db: Session, datos: MaquinaCreate):
        db_maquina = MaquinaModel(
            nombre=datos.nombre,
            estado=datos.estado,
            fecha_adquisicion=datos.fecha_adquisicion,
        )
        db.add(db_maquina)
        db.commit()
        db.refresh(db_maquina)
        return db_maquina

    @staticmethod
    def actualizar_estado(
        db: Session, maquina: MaquinaModel, nuevo_estado: str
    ):
        maquina.estado = nuevo_estado
        db.commit()
        db.refresh(maquina)
        return maquina

    @staticmethod
    def registrar_mantenimiento(
        db: Session, maquina: MaquinaModel, datos: MantenimientoCreate
    ):
        db_mantenimiento = MantenimientoModel(
            fecha=datos.fecha,
            descripcion=datos.descripcion,
            costo=datos.costo,
            estado=datos.estado,
            maquina=maquina,
        )
        db.add(db_mantenimiento)
        db.commit()
        db.refresh(db_mantenimiento)
        return db_mantenimiento
