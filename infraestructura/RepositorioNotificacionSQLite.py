import sqlite3
from typing import List, Optional, Union
from uuid import UUID

from aplicacion.puertos.RepositorioNotificacion import RepositorioNotificacion
from infraestructura.ConexionSQLite import ConexionSQLite

try:
    from dominio.Notificacion import Notificacion
except ImportError:
    class Notificacion:
        """Clase de dominio Notificacion (fallback si no está disponible en dominio)."""
        def __init__(
            self,
            id_notificacion: Optional[Union[str, UUID]] = None,
            destinatario: str = "",
            mensaje: str = "",
            fecha: str = "",
            tipo: str = "general",
            **kwargs,
        ):
            self.id = id_notificacion or kwargs.get("id")
            self.destinatario = destinatario
            self.mensaje = mensaje
            self.fecha = fecha
            self.tipo = tipo


class RepositorioNotificacionSQLite(RepositorioNotificacion):
    """
    Implementación del puerto RepositorioNotificacion usando SQLite3.
    """

    def __init__(self, conexion_o_path: Union[str, ConexionSQLite] = "sistema_prestamos.db"):
        if isinstance(conexion_o_path, ConexionSQLite):
            self.conexion_sqlite = conexion_o_path
        else:
            self.conexion_sqlite = ConexionSQLite(conexion_o_path)

    def _get_connection(self) -> sqlite3.Connection:
        return self.conexion_sqlite.obtener_conexion()

    def guardar(self, notificacion: Notificacion) -> None:
        """Inserta o actualiza una notificación en SQLite."""
        notif_id = str(getattr(notificacion, "id_notificacion", getattr(notificacion, "id", "")))
        tipo = str(getattr(notificacion, "tipo", "general"))
        destinatario = str(getattr(notificacion, "destinatario", ""))
        mensaje = str(getattr(notificacion, "mensaje", ""))
        fecha = str(getattr(notificacion, "fecha", ""))

        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO notificaciones (id, tipo, destinatario, mensaje, fecha)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (notif_id, tipo, destinatario, mensaje, fecha),
                )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def _reconstruir_notificacion(self, row: sqlite3.Row) -> Notificacion:
        try:
            id_val = UUID(str(row["id"]))
        except Exception:
            id_val = row["id"]

        try:
            return Notificacion(
                id_notificacion=id_val,
                mensaje=row["mensaje"],
                destinatario=row["destinatario"],
                fecha=row["fecha"],
                tipo=row["tipo"],
            )
        except TypeError:
            return Notificacion(
                id=id_val,
                mensaje=row["mensaje"],
                destinatario=row["destinatario"],
                fecha=row["fecha"],
                tipo=row["tipo"],
            )

    def buscar_por_id(self, id: Union[str, UUID]) -> Optional[Notificacion]:
        """Busca una notificación por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, tipo, destinatario, mensaje, fecha FROM notificaciones WHERE id = ?",
                (id_str,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return self._reconstruir_notificacion(row)
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def buscarPorId(self, id: Union[str, UUID]) -> Optional[Notificacion]:
        """Alias para cumplir con la interfaz del puerto RepositorioNotificacion."""
        return self.buscar_por_id(id)

    def obtener_todos(self) -> List[Notificacion]:
        """Obtiene todas las notificaciones registradas en SQLite."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, tipo, destinatario, mensaje, fecha FROM notificaciones")
            rows = cursor.fetchall()
            return [self._reconstruir_notificacion(row) for row in rows]
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtenerTodos(self) -> List[Notificacion]:
        """Alias para cumplir con la interfaz del puerto RepositorioNotificacion."""
        return self.obtener_todos()

    def eliminar(self, id: Union[str, UUID]) -> None:
        """Elimina una notificación por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM notificaciones WHERE id = ?", (id_str,))
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()
