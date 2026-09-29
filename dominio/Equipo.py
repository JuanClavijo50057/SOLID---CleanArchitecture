from abc import ABC, abstractmethod
from decimal import Decimal
from dominio.Enums import EstadoEquipo

class Equipo(ABC):
    def __init__(self, id_equipo: str, tarifa_diaria: Decimal, plazo_prestamo: int, estado: EstadoEquipo = EstadoEquipo.DISPONIBLE):
        self.id = str(id_equipo)
        self.estado = estado
        self.tarifa_diaria = tarifa_diaria
        self.plazo_prestamo = plazo_prestamo