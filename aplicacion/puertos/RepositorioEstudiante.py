from abc import ABC, abstractmethod
from typing import List
from dominio.Estudiante import Estudiante

class RepositorioEstudiante(ABC):
    """
    Puerto (Interfaz) para el repositorio de estudiantes.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscarPorId(self, id: str) -> Estudiante:
        """Busca un estudiante por su identificador único."""
        pass

    @abstractmethod
    def obtenerTodos(self) -> List[Estudiante]:
        """Retorna todos los estudiantes registrados."""
        pass

    @abstractmethod
    def guardar(self, estudiante: Estudiante) -> None:
        """Guarda o actualiza un estudiante."""
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        """Elimina un estudiante por su identificador único."""
        pass