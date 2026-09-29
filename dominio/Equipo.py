from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID
from dominio.Enums import EstadoEquipo

class Equipo(ABC):
    def __init__(self, id: UUID, tarifa_diaria: Decimal, plazo_prestamo: int, estado: EstadoEquipo = EstadoEquipo.DISPONIBLE):
        self.id = id
        self.estado = estado
        self.tarifa_diaria = tarifa_diaria
        self.plazo_prestamo = plazo_prestamo