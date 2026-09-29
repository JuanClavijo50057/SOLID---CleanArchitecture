from dominio.Equipo import Equipo
from dominio.Enums import EstadoEquipo
from decimal import Decimal

class Portatil(Equipo):
    # R3 y R5
    TARIFA_DIARIA = Decimal('5000.00')
    PLAZO_PRESTAMO = 3

    def __init__(self, id_equipo: str, estado: EstadoEquipo = EstadoEquipo.DISPONIBLE):
        super().__init__(
            id_equipo=id_equipo,
            tarifa_diaria=self.TARIFA_DIARIA,
            plazo_prestamo=self.PLAZO_PRESTAMO,
            estado=estado
        )