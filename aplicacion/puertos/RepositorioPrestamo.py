from abc import ABC, abstractmethod
from typing import List, Optional

try:
    from dominio.Prestamo import Prestamo
except ImportError:
    from typing import Any as Prestamo


class RepositorioPrestamo(ABC):
    """
    Puerto (Interfaz) para el repositorio de préstamos.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscarPorId(self, id: str) -> Optional[Prestamo]:
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

    # Aliases compatibles con convenciones PEP8
    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
