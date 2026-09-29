from typing import Dict, List, Optional, Union
from uuid import UUID
from aplicacion.puertos.RepositorioPrestamo import RepositorioPrestamo
from dominio.Prestamo import Prestamo
from dominio.Enums import EstadoPrestamo, EstadoMulta


class RepositorioPrestamoLocal(RepositorioPrestamo):
    """
    Implementación en memoria (local) del puerto RepositorioPrestamo.
    """

    def __init__(self):
        self._datos: Dict[str, Prestamo] = {}

    def guardar(self, prestamo: Prestamo) -> None:
        p_id = str(prestamo.id)
        self._datos[p_id] = prestamo

    def buscar_por_id(self, id: Union[str, UUID]) -> Optional[Prestamo]:
        return self._datos.get(str(id))

    def buscarPorId(self, id: Union[str, UUID]) -> Optional[Prestamo]:
        return self.buscar_por_id(id)

    def obtener_todos(self) -> List[Prestamo]:
        return list(self._datos.values())

    def obtenerTodos(self) -> List[Prestamo]:
        return self.obtener_todos()

    def eliminar(self, id: Union[str, UUID]) -> None:
        id_str = str(id)
        if id_str in self._datos:
            del self._datos[id_str]

    def obtener_activos_por_estudiante(self, id_estudiante: Union[str, UUID]) -> List[Prestamo]:
        id_str = str(id_estudiante)
        return [
            p for p in self._datos.values()
            if str(getattr(p, "estudiante_id", getattr(getattr(p, "estudiante", None), "id", ""))) == id_str
            and (p.estado == EstadoPrestamo.ACTIVO or getattr(p.estado, "value", None) == "Activo")
        ]

    def tiene_multas_pendientes(self, id_estudiante: Union[str, UUID]) -> bool:
        id_str = str(id_estudiante)
        for p in self._datos.values():
            p_est_id = str(getattr(p, "estudiante_id", getattr(getattr(p, "estudiante", None), "id", "")))
            if p_est_id == id_str:
                multa = getattr(p, "multa", None)
                if multa and (getattr(multa, "estado", None) == EstadoMulta.PENDIENTE or getattr(getattr(multa, "estado", None), "value", None) == "Pendiente"):
                    return True
        return False
