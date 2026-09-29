from abc import ABC, abstractmethod
from typing import List
from dominio.Notificacion import Notificacion

class RepositorioNotificacion(ABC):
    """
    Puerto (Interfaz) para el repositorio de notificaciones.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscar_por_id(self, id: str) -> Notificacion:
        """Busca una notificación por su identificador único."""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Notificacion]:
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

    def buscarPorId(self, id: str) -> Notificacion:
        return self.buscar_por_id(id)

    def obtenerTodos(self) -> List[Notificacion]:
        return self.obtener_todos()
