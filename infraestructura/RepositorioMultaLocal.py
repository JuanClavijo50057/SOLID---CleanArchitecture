from typing import Dict, List, Optional, Union
from uuid import UUID
from aplicacion.puertos.RepositorioMulta import RepositorioMulta
from dominio.Multa import Multa
from dominio.Enums import EstadoMulta


class RepositorioMultaLocal(RepositorioMulta):
    """
    Implementación en memoria (local) del puerto RepositorioMulta.
    """

    def __init__(self):
        self._datos: Dict[str, Multa] = {}

    def guardar(self, multa: Multa) -> None:
        m_id = str(getattr(multa, "id_multa", getattr(multa, "id", "")))
        self._datos[m_id] = multa

    def buscar_por_id(self, id: Union[str, UUID]) -> Optional[Multa]:
        return self._datos.get(str(id))

    def buscarPorId(self, id: Union[str, UUID]) -> Optional[Multa]:
        return self.buscar_por_id(id)

    def obtener_todos(self) -> List[Multa]:
        return list(self._datos.values())

    def obtenerTodos(self) -> List[Multa]:
        return self.obtener_todos()

    def eliminar(self, id: Union[str, UUID]) -> None:
        id_str = str(id)
        if id_str in self._datos:
            del self._datos[id_str]

    def tiene_multas_pendientes(self, id_estudiante: Union[str, UUID]) -> bool:
        # Método auxiliar para casos de uso
        return False
