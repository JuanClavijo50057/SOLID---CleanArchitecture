from typing import Dict, List
from aplicacion.puertos.RepositorioEstudiante import RepositorioEstudiante

try:
    from dominio.Estudiante import Estudiante
except ImportError:
    class Estudiante:
        def __init__(self, id, nombre, codigo, correo):
            self.id = id
            self.nombre = nombre
            self.codigo = codigo
            self.correo = correo


class RepositorioEstudianteLocal(RepositorioEstudiante):
    """
    Implementación en memoria (local) del puerto RepositorioEstudiante.
    Ideal para pruebas unitarias y entornos sin base de datos persistente.
    """

    def __init__(self):
        self._datos: Dict[str, Estudiante] = {}

    def guardar(self, estudiante: Estudiante) -> None:
        est_id = str(getattr(estudiante, "id", ""))
        self._datos[est_id] = estudiante

    def buscar_por_id(self, id: str) -> Estudiante:
        return self._datos.get(str(id))

    buscarPorId = buscar_por_id

    def obtener_todos(self) -> List[Estudiante]:
        return list(self._datos.values())

    obtenerTodos = obtener_todos

    def eliminar(self, id: str) -> None:
        id_str = str(id)
        if id_str in self._datos:
            del self._datos[id_str]

    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
