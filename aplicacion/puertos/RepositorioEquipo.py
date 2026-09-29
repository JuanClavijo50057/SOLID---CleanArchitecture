from abc import ABC, abstractmethod
from typing import List, Optional

try:
    from dominio.Equipo import Equipo
except ImportError:
    from typing import Any as Equipo


class RepositorioEquipo(ABC):
    """
    Puerto (Interfaz) para el repositorio de equipos.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscarPorId(self, id: str) -> Optional[Equipo]:
        """Busca un equipo por su identificador único."""
        pass

    @abstractmethod
    def obtenerTodos(self) -> List[Equipo]:
        """Retorna todos los equipos registrados."""
        pass

    @abstractmethod
    def guardar(self, equipo: Equipo) -> None:
        """Guarda o actualiza un equipo."""
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        """Elimina un equipo por su identificador único."""
        pass

    # Aliases compatibles con convenciones PEP8
    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
