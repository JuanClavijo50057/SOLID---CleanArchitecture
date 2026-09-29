import sqlite3
from typing import List, Optional, Union
from uuid import UUID
from decimal import Decimal

from aplicacion.puertos.RepositorioMulta import RepositorioMulta
from infraestructura.ConexionSQLite import ConexionSQLite

try:
    from dominio.Multa import Multa
except ImportError:
    class Multa:
        def __init__(self, id=None, tarifa=None, total=None, estado=None):
            self.id = id
            self.tarifa = tarifa
            self.total = total
            self.estado = estado

        def __repr__(self):
            return f"<Multa id={self.id} tarifa={self.tarifa} total={self.total} estado={self.estado}>"

try:
    from dominio.Enums import EstadoMulta
except ImportError:
    from enum import Enum

    class EstadoMulta(Enum):
        PAGADA = "Pagada"
        PENDIENTE = "Pendiente"


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
        m_id = str(getattr(multa, "id", ""))
        tarifa = float(getattr(multa, "tarifa", 0.0))
        total = float(getattr(multa, "total", 0.0))
        estado = getattr(multa, "estado", EstadoMulta.PENDIENTE)
        estado_val = estado.value if hasattr(estado, "value") else str(estado)

        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO multas (id, tarifa, total, estado)
                    VALUES (?, ?, ?, ?)
                    """,
                    (m_id, tarifa, total, estado_val),
                )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def buscarPorId(self, id: str) -> Optional[Multa]:
        """Busca una multa por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, tarifa, total, estado FROM multas WHERE id = ?",
                (id_str,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            try:
                id_val = UUID(row["id"])
            except Exception:
                id_val = row["id"]

            try:
                estado = EstadoMulta(row["estado"])
            except Exception:
                estado = row["estado"]

            multa = Multa(
                id=id_val,
                tarifa=Decimal(str(row["tarifa"])),
                total=Decimal(str(row["total"])),
            )
            multa.estado = estado
            return multa
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtenerTodos(self) -> List[Multa]:
        """Obtiene todas las multas registradas en SQLite."""
        multas: List[Multa] = []
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, tarifa, total, estado FROM multas")
            rows = cursor.fetchall()
            for row in rows:
                try:
                    id_val = UUID(row["id"])
                except Exception:
                    id_val = row["id"]

                try:
                    estado = EstadoMulta(row["estado"])
                except Exception:
                    estado = row["estado"]

                m = Multa(
                    id=id_val,
                    tarifa=Decimal(str(row["tarifa"])),
                    total=Decimal(str(row["total"])),
                )
                m.estado = estado
                multas.append(m)
            return multas
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

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

    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
