from typing import List
from aplicacion.puertos.RepositorioPrestamo import RepositorioPrestamo
from dominio.Prestamo import Prestamo
from dominio.Enums import EstadoPrestamo


class RepositorioPrestamoLocal(RepositorioPrestamo):
    """
    Implementación en memoria (local) del puerto RepositorioPrestamo.
    """

    def __init__(self):
        self._datos: List[Prestamo] = []

    def guardar(self, prestamo: Prestamo) -> None:
        existente = self.buscar_por_id(prestamo.id)
        if existente is not None:
            self._datos[self._datos.index(existente)] = prestamo
            return
        self._datos.append(prestamo)

    def buscar_por_id(self, id: str) -> Prestamo:
        return next((p for p in self._datos if str(p.id) == str(id)), None)

    def buscarPorId(self, id: str) -> Prestamo:
        return self.buscar_por_id(id)

    def obtener_todos(self) -> List[Prestamo]:
        return list(self._datos)

    def obtenerTodos(self) -> List[Prestamo]:
        return self.obtener_todos()

    def eliminar(self, id: str) -> None:
        self._datos = [p for p in self._datos if str(p.id) != str(id)]

    def obtener_activos_por_estudiante(self, id_estudiante: str) -> List[Prestamo]:
        id_str = str(id_estudiante)
        return [
            p for p in self._datos
            if str(getattr(p, "estudiante_id", getattr(getattr(p, "estudiante", None), "id", ""))) == id_str
            and (p.estado == EstadoPrestamo.ACTIVO or getattr(p.estado, "value", None) == "Activo")
        ]

