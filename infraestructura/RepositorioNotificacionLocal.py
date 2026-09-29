from typing import Dict, List
from aplicacion.puertos.RepositorioNotificacion import RepositorioNotificacion

try:
    from dominio.Notificacion import Notificacion
except ImportError:
    class Notificacion:
        def __init__(self, id=None, mensaje=None, destinatario=None, fecha=None, tipo=None):
            self.id = id
            self.mensaje = mensaje
            self.destinatario = destinatario
            self.fecha = fecha
            self.tipo = tipo


class RepositorioNotificacionLocal(RepositorioNotificacion):
    """
    Implementación en memoria (local) del puerto RepositorioNotificacion.
    """

    def __init__(self):
        self._datos: Dict[str, Notificacion] = {}

    def guardar(self, notificacion: Notificacion) -> None:
        notif_id = str(getattr(notificacion, "id", ""))
        self._datos[notif_id] = notificacion

    def buscarPorId(self, id: str) -> Notificacion:
        return self._datos.get(str(id))

    def obtenerTodos(self) -> List[Notificacion]:
        return list(self._datos.values())

    def eliminar(self, id: str) -> None:
        id_str = str(id)
        if id_str in self._datos:
            del self._datos[id_str]

    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
