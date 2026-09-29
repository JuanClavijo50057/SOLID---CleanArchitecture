import sqlite3
from typing import List, Union

from aplicacion.puertos.RepositorioEstudiante import RepositorioEstudiante
from infraestructura.ConexionSQLite import ConexionSQLite
from dominio.Estudiante import Estudiante


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
        est_id = str(getattr(estudiante, "id_estudiante", getattr(estudiante, "id", "")))
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

    def _reconstruir_estudiante(self, row: sqlite3.Row) -> Estudiante:
        return Estudiante(
            id_estudiante=str(row["id"]),
            nombre=row["nombre"],
            codigo=row["codigo"],
            correo=row["correo"],
        )

    def buscar_por_id(self, id: str) -> Estudiante:
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
            return self._reconstruir_estudiante(row)
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def buscarPorId(self, id: str) -> Estudiante:
        """Alias para cumplir con la interfaz del puerto RepositorioEstudiante."""
        return self.buscar_por_id(id)

    def obtener_todos(self) -> List[Estudiante]:
        """Obtiene todos los estudiantes registrados en SQLite."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, codigo, correo FROM estudiantes")
            rows = cursor.fetchall()
            return [self._reconstruir_estudiante(row) for row in rows]
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtenerTodos(self) -> List[Estudiante]:
        """Alias para cumplir con la interfaz del puerto RepositorioEstudiante."""
        return self.obtener_todos()

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
