from typing import Dict, List, Optional
from aplicacion.puertos.RepositorioPrestamo import RepositorioPrestamo
from dominio.Prestamo import Prestamo


class RepositorioPrestamoLocal(RepositorioPrestamo):
    """
    Implementación en memoria (local) del puerto RepositorioPrestamo.
    """

    def __init__(self):
        self._datos: Dict[str, Prestamo] = {}

    def guardar(self, prestamo: Prestamo) -> None:
        p_id = str(prestamo.id)
        self._datos[p_id] = prestamo

    def buscarPorId(self, id: str) -> Optional[Prestamo]:
        return self._datos.get(str(id))

    def obtenerTodos(self) -> List[Prestamo]:
        return list(self._datos.values())

    def eliminar(self, id: str) -> None:
        id_str = str(id)
        if id_str in self._datos:
            del self._datos[id_str]

    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
