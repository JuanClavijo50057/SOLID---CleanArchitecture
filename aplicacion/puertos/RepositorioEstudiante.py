from abc import ABC, abstractmethod
from typing import List, Optional

try:
    from dominio.Estudiante import Estudiante
except ImportError:
    from typing import Any as Estudiante


class RepositorioEstudiante(ABC):
    """
    Puerto (Interfaz) para el repositorio de estudiantes.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscarPorId(self, id: str) -> Optional[Estudiante]:
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

    # Aliases compatibles con convenciones PEP8
    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
