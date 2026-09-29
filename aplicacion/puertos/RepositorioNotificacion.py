from abc import ABC, abstractmethod
from typing import List, Optional

try:
    from dominio.Notificacion import Notificacion
except ImportError:
    from typing import Any as Notificacion


class RepositorioNotificacion(ABC):
    """
    Puerto (Interfaz) para el repositorio de notificaciones.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscarPorId(self, id: str) -> Optional[Notificacion]:
        """Busca una notificación por su identificador único."""
        pass

    @abstractmethod
    def obtenerTodos(self) -> List[Notificacion]:
        """Retorna todas las notificaciones registradas."""
        pass

    @abstractmethod
    def guardar(self, notificacion: Notificacion) -> None:
        """Guarda o actualiza una notificación."""
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        """Elimina una notificación por su identificador único."""
        pass

    # Aliases compatibles con convenciones PEP8
    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
