import sqlite3
from typing import List, Union
from decimal import Decimal

from aplicacion.puertos.RepositorioMulta import RepositorioMulta
from infraestructura.ConexionSQLite import ConexionSQLite
from dominio.Multa import Multa
from dominio.Enums import EstadoMulta


class RepositorioMultaSQLite(RepositorioMulta):
    """
    Implementación del puerto RepositorioMulta usando SQLite3.
    """

    def __init__(self, conexion_o_path: Union[str, ConexionSQLite] = "sistema_prestamos.db"):
        if isinstance(conexion_o_path, ConexionSQLite):
            self.conexion_sqlite = conexion_o_path
        else:
            self.conexion_sqlite = ConexionSQLite(conexion_o_path)

    def _get_connection(self) -> sqlite3.Connection:
        return self.conexion_sqlite.obtener_conexion()

    def guardar(self, multa: Multa) -> None:
        """Inserta o actualiza una multa en SQLite."""
        m_id = str(getattr(multa, "id_multa", getattr(multa, "id", "")))
        tarifa_str = str(Decimal(str(multa.tarifa)))
        total_str = str(Decimal(str(multa.total)))
        estado = getattr(multa, "estado", EstadoMulta.PENDIENTE)
        estado_val = estado.value if hasattr(estado, "value") else str(estado)

        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO multas (
                        id, estudiante_id, tarifa, total, estado
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (m_id, str(getattr(multa, "estudiante_id", "")), tarifa_str, total_str, estado_val),
                )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def _reconstruir_multa(self, row: sqlite3.Row) -> Multa:
        estado_raw = row["estado"]
        try:
            estado = EstadoMulta(estado_raw)
        except ValueError:
            try:
                estado = EstadoMulta[estado_raw]
            except KeyError:
                estado = EstadoMulta.PENDIENTE

        tarifa_dec = Decimal(str(row["tarifa"]))
        total_dec = Decimal(str(row["total"]))

        return Multa(
            id_multa=str(row["id"]),
            tarifa=tarifa_dec,
            total=total_dec,
            estado=estado,
            estudiante_id=str(row["estudiante_id"]),
        )

    def buscar_por_id(self, id: str) -> Multa:
        """Busca una multa por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, estudiante_id, tarifa, total, estado FROM multas WHERE id = ?",
                (id_str,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return self._reconstruir_multa(row)
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def buscarPorId(self, id: str) -> Multa:
        """Alias para cumplir con la interfaz del puerto RepositorioMulta."""
        return self.buscar_por_id(id)

    def obtener_todos(self) -> List[Multa]:
        """Obtiene todas las multas registradas en SQLite."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, estudiante_id, tarifa, total, estado FROM multas")
            rows = cursor.fetchall()
            return [self._reconstruir_multa(row) for row in rows]
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtenerTodos(self) -> List[Multa]:
        """Alias para cumplir con la interfaz del puerto RepositorioMulta."""
        return self.obtener_todos()

    def eliminar(self, id: str) -> None:
        """Elimina una multa por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM multas WHERE id = ?", (id_str,))
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def tiene_multas_pendientes(self, id_estudiante: str) -> bool:
        """Retorna True si el estudiante tiene al menos una multa en estado PENDIENTE."""
        id_str = str(id_estudiante)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 1 FROM multas m
                WHERE m.estudiante_id = ? AND (m.estado = ? OR m.estado = ?)
                LIMIT 1
                """,
                (id_str, EstadoMulta.PENDIENTE.value, "PENDIENTE"),
            )
            return cursor.fetchone() is not None
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()
