from typing import Dict, List, Optional
from aplicacion.puertos.RepositorioEquipo import RepositorioEquipo
from dominio.Equipo import Equipo


class RepositorioEquipoLocal(RepositorioEquipo):
    """
    Implementación en memoria (local) del puerto RepositorioEquipo.
    """

    def __init__(self):
        self._datos: Dict[str, Equipo] = {}

    def guardar(self, equipo: Equipo) -> None:
        eq_id = str(getattr(equipo, "id_equipo", getattr(equipo, "id", "")))
        self._datos[eq_id] = equipo

    def buscarPorId(self, id: str) -> Optional[Equipo]:
        return self._datos.get(str(id))

    def obtenerTodos(self) -> List[Equipo]:
        return list(self._datos.values())

    def eliminar(self, id: str) -> None:
        id_str = str(id)
        if id_str in self._datos:
            del self._datos[id_str]

    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
