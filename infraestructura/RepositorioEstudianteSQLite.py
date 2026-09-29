import sqlite3
from typing import List, Optional, Union
from uuid import UUID

from aplicacion.puertos.RepositorioEstudiante import RepositorioEstudiante
from infraestructura.ConexionSQLite import ConexionSQLite

try:
    from dominio.Estudiante import Estudiante
except ImportError:
    class Estudiante:
        def __init__(self, id, nombre, codigo, correo):
            self.id = id
            self.nombre = nombre
            self.codigo = codigo
            self.correo = correo

        def __repr__(self):
            return f"<Estudiante id={self.id} nombre={self.nombre} codigo={self.codigo} correo={self.correo}>"


class RepositorioEstudianteSQLite(RepositorioEstudiante):
    """
    Implementación del puerto RepositorioEstudiante usando SQLite3.
    """

    def __init__(self, conexion_o_path: Union[str, ConexionSQLite] = "sistema_prestamos.db"):
        if isinstance(conexion_o_path, ConexionSQLite):
            self.conexion_sqlite = conexion_o_path
        else:
            self.conexion_sqlite = ConexionSQLite(conexion_o_path)

    def _get_connection(self) -> sqlite3.Connection:
        return self.conexion_sqlite.obtener_conexion()

    def guardar(self, estudiante: Estudiante) -> None:
        """Inserta o actualiza un estudiante en SQLite."""
        est_id = str(getattr(estudiante, "id", ""))
        nombre = str(getattr(estudiante, "nombre", ""))
        codigo = str(getattr(estudiante, "codigo", ""))
        correo = str(getattr(estudiante, "correo", ""))

        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO estudiantes (id, nombre, codigo, correo)
                    VALUES (?, ?, ?, ?)
                    """,
                    (est_id, nombre, codigo, correo),
                )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def buscarPorId(self, id: str) -> Optional[Estudiante]:
        """Busca un estudiante por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, codigo, correo FROM estudiantes WHERE id = ?",
                (id_str,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            try:
                id_val = UUID(row["id"])
            except Exception:
                id_val = row["id"]
            return Estudiante(
                id=id_val,
                nombre=row["nombre"],
                codigo=row["codigo"],
                correo=row["correo"],
            )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtenerTodos(self) -> List[Estudiante]:
        """Obtiene todos los estudiantes registrados en SQLite."""
        estudiantes: List[Estudiante] = []
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, codigo, correo FROM estudiantes")
            rows = cursor.fetchall()
            for row in rows:
                try:
                    id_val = UUID(row["id"])
                except Exception:
                    id_val = row["id"]
                estudiantes.append(
                    Estudiante(
                        id=id_val,
                        nombre=row["nombre"],
                        codigo=row["codigo"],
                        correo=row["correo"],
                    )
                )
            return estudiantes
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def eliminar(self, id: str) -> None:
        """Elimina un estudiante por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM estudiantes WHERE id = ?", (id_str,))
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
