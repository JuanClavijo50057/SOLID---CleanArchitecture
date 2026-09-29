from abc import ABC, abstractmethod
from typing import List
from dominio.Prestamo import Prestamo

class RepositorioPrestamo(ABC):
    """
    Puerto (Interfaz) para el repositorio de préstamos.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscar_por_id(self, id: str) -> Prestamo:
        """Busca un préstamo por su identificador único."""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Prestamo]:
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

    @abstractmethod
    def obtener_activos_por_estudiante(self, id_estudiante: str) -> List[Prestamo]:
        """
        Retorna la lista de préstamos que el estudiante aún no ha devuelto 
        (EstadoPrestamo.ACTIVO).
        """
        pass

    def buscarPorId(self, id: str) -> Prestamo:
        return self.buscar_por_id(id)

    def obtenerTodos(self) -> List[Prestamo]:
        return self.obtener_todos()
