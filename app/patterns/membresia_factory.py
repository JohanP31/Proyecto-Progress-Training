"""Patrón Factory Method: crea membresías según su tipo."""

from datetime import date, timedelta

from app.models.membresia import MembresiaModel

# Datos de cada tipo de membresía.
# OJO: los valores son de ejemplo. Hay que confirmarlos con el gimnasio.
TIPOS_MEMBRESIA = {
    # 30 días contando el día de inicio
    "mensualidad": {"dias": 30, "valor": 80000},
    # Solo sirve el mismo día
    "ingreso_unico": {"dias": 1, "valor": 10000},
}


class MembresiaFactory:
    """Sabe cómo armar cada tipo de membresía."""

    @staticmethod
    def crear(tipo: str, fecha_inicio: date) -> MembresiaModel:
        """Devuelve una membresía con su fecha de fin y su valor."""
        if tipo not in TIPOS_MEMBRESIA:
            raise ValueError(f"Tipo de membresía no válido: {tipo}")

        datos = TIPOS_MEMBRESIA[tipo]
        # Se resta 1 porque el día de inicio también cuenta
        fecha_fin = fecha_inicio + timedelta(days=datos["dias"] - 1)
        return MembresiaModel(
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            valor=datos["valor"],
        )
