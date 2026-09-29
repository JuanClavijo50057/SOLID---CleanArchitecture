from abc import ABC, abstractmethod
from datetime import date

class ProveedorFecha(ABC):
    """
    Puerto (Interfaz) para proveer la fecha actual del sistema.
    Facilita el testing mediante mocks de tiempo.
    """

    @abstractmethod
    def hoy(self) -> date:
        """Retorna la fecha actual."""
        pass