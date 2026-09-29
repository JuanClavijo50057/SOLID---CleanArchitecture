from abc import ABC, abstractmethod
from typing import List, Optional

try:
    from dominio.Multa import Multa
except ImportError:
    from typing import Any as Multa


class RepositorioMulta(ABC):
    """
    Puerto (Interfaz) para el repositorio de multas.
    Define las operaciones que cualquier adaptador de persistencia debe implementar.
    """

    @abstractmethod
    def buscarPorId(self, id: str) -> Optional[Multa]:
        """Busca una multa por su identificador único."""
        pass

    @abstractmethod
    def obtenerTodos(self) -> List[Multa]:
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

    # Aliases compatibles con convenciones PEP8
    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
