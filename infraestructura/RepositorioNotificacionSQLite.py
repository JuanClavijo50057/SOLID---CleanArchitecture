import sqlite3
from typing import List, Optional, Union
from uuid import UUID

from aplicacion.puertos.RepositorioNotificacion import RepositorioNotificacion
from infraestructura.ConexionSQLite import ConexionSQLite

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

        def __repr__(self):
            return (
                f"<Notificacion id={self.id} destinatario={self.destinatario} "
                f"mensaje={self.mensaje} fecha={self.fecha}>"
            )


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
        notif_id = str(getattr(notificacion, "id", ""))
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

    def buscarPorId(self, id: str) -> Optional[Notificacion]:
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

            try:
                id_val = UUID(row["id"])
            except Exception:
                id_val = row["id"]

            return Notificacion(
                id=id_val,
                mensaje=row["mensaje"],
                destinatario=row["destinatario"],
                fecha=row["fecha"],
                tipo=row["tipo"],
            )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtenerTodos(self) -> List[Notificacion]:
        """Obtiene todas las notificaciones registradas en SQLite."""
        notificaciones: List[Notificacion] = []
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, tipo, destinatario, mensaje, fecha FROM notificaciones"
            )
            rows = cursor.fetchall()
            for row in rows:
                try:
                    id_val = UUID(row["id"])
                except Exception:
                    id_val = row["id"]

                notificaciones.append(
                    Notificacion(
                        id=id_val,
                        mensaje=row["mensaje"],
                        destinatario=row["destinatario"],
                        fecha=row["fecha"],
                        tipo=row["tipo"],
                    )
                )
            return notificaciones
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def eliminar(self, id: str) -> None:
        """Elimina una notificación por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM notificaciones WHERE id = ?", (id_str,))
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
