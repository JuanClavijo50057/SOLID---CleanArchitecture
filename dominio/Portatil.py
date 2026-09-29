from uuid import UUID
from dominio.Equipo import Equipo
from dominio.Enums import EstadoEquipo

class Portatil(Equipo):
    # R3 y R5
    TARIFA_DIARIA = 5000
    PLAZO_PRESTAMO = 3

    def __init__(self, id_equipo: UUID, estado: EstadoEquipo = EstadoEquipo.DISPONIBLE):
        super().__init__(
            id_equipo=id_equipo,
            tarifa_diaria=self.TARIFA_DIARIA_PORTATIL,
            plazo_prestamo=self.PLAZO_PRESTAMO_PORTATIL,
            estado=estado
        )