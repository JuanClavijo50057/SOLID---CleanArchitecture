from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal

class Prestable(ABC):
    """
    Interfaz que define el comportamiento esperado para
    entidades que manejan lógicas de préstamos y devoluciones.
    """
    
    @abstractmethod
    def calcular_dias_retraso(self, fecha_devolucion: date) -> int:
        pass

    @abstractmethod
    def calcular_multa(self, dias_retraso: int) -> Decimal:
        pass