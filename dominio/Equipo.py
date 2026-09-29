from abc import ABC, abstractmethod
from uuid import UUID
from dominio.Enums import EstadoEquipo

class Equipo(ABC):
    def __init__(self, id_equipo: UUID, tarifa_diaria: float, plazo_prestamo: int, estado: EstadoEquipo = EstadoEquipo.DISPONIBLE):
        self.id_equipo = id_equipo
        self.estado = estado
        self.tarifa_diaria = tarifa_diaria
        self.plazo_prestamo = plazo_prestamo

    @abstractmethod
    def calcular_multa(self, dias: int) -> float:
        pass