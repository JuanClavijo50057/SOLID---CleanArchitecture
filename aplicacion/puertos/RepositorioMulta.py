from abc import ABC, abstractmethod
from typing import List
from dominio.Multa import Multa

class RepositorioMulta(ABC):
    """
    Puerto (Interfaz) para el repositorio de multas.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscar_por_id(self, id: str) -> Multa:
        """Busca una multa por su identificador único."""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Multa]:
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

    @abstractmethod
    def tiene_multas_pendientes(self, id_estudiante: str) -> bool:
        """Indica si el estudiante tiene una multa pendiente."""
        pass

    def buscarPorId(self, id: str) -> Multa:
        return self.buscar_por_id(id)

    def obtenerTodos(self) -> List[Multa]:
        return self.obtener_todos()