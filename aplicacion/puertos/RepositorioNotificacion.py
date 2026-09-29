from abc import ABC, abstractmethod
from typing import List
from dominio.Notificacion import Notificacion

class RepositorioNotificacion(ABC):
    """
    Puerto (Interfaz) para el repositorio de notificaciones.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscarPorId(self, id: str) -> Notificacion:
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
