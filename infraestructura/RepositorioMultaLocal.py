from typing import Dict, List, Optional
from aplicacion.puertos.RepositorioMulta import RepositorioMulta

try:
    from dominio.Multa import Multa
except ImportError:
    class Multa:
        def __init__(self, id=None, tarifa=None, total=None, estado=None):
            self.id = id
            self.tarifa = tarifa
            self.total = total
            self.estado = estado


class RepositorioMultaLocal(RepositorioMulta):
    """
    Implementación en memoria (local) del puerto RepositorioMulta.
    """

    def __init__(self):
        self._datos: Dict[str, Multa] = {}

    def guardar(self, multa: Multa) -> None:
        m_id = str(getattr(multa, "id", ""))
        self._datos[m_id] = multa

    def buscarPorId(self, id: str) -> Optional[Multa]:
        return self._datos.get(str(id))

    def obtenerTodos(self) -> List[Multa]:
        return list(self._datos.values())

    def eliminar(self, id: str) -> None:
        id_str = str(id)
        if id_str in self._datos:
            del self._datos[id_str]

    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
