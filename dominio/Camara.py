from uuid import UUID
from decimal import Decimal
from dominio.Equipo import Equipo
from dominio.Enums import EstadoEquipo

class Camara(Equipo):
    # Reglas de negocio para Cámara (R3 y R5)
    TARIFA_DIARIA = Decimal('8000.00')
    PLAZO_PRESTAMO = 2

    def __init__(self, id_equipo: UUID, estado: EstadoEquipo = EstadoEquipo.DISPONIBLE):
        super().__init__(
            id_equipo=id_equipo,
            tarifa_diaria=self.TARIFA_DIARIA,
            plazo_prestamo=self.PLAZO_PRESTAMO,
            estado=estado
        )