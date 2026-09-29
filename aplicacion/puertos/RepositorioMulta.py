from abc import ABC, abstractmethod
from typing import List
from dominio.Multa import Multa

class RepositorioMulta(ABC):
    """
    Puerto (Interfaz) para el repositorio de multas.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscarPorId(self, id: str) -> Multa:
        """Busca una multa por su identificador único."""
        pass

    @abstractmethod
    def obtenerTodos(self) -> List[Multa]:
        """Retorna todas las multas registradas."""
        pass

    @abstractmethod
    def guardar(self, multa: Multa) -> None:
        """Guarda o actualiza una multa."""
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        """Elimina una multa por su identificador único."""
        pass