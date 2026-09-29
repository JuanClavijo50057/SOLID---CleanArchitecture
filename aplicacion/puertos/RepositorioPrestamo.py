from abc import ABC, abstractmethod
from typing import List
from dominio.Prestamo import Prestamo

class RepositorioPrestamo(ABC):
    """
    Puerto (Interfaz) para el repositorio de préstamos.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscarPorId(self, id: str) -> Prestamo:
        """Busca un préstamo por su identificador único."""
        pass

    @abstractmethod
    def obtenerTodos(self) -> List[Prestamo]:
        """Retorna todos los préstamos registrados."""
        pass

    @abstractmethod
    def guardar(self, prestamo: Prestamo) -> None:
        """Guarda o actualiza un préstamo."""
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        """Elimina un préstamo por su identificador único."""
        pass