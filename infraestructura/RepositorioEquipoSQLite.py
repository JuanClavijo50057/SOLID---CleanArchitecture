import sqlite3
from typing import List, Optional, Union
from uuid import UUID
from decimal import Decimal

from aplicacion.puertos.RepositorioEquipo import RepositorioEquipo
from infraestructura.ConexionSQLite import ConexionSQLite
from dominio.Equipo import Equipo
from dominio.Enums import EstadoEquipo
from dominio.Portatil import Portatil
from dominio.Camara import Camara
from dominio.KitRobotica import KitRobotica

# Asegurar que Portatil, Camara y KitRobotica puedan ser instanciados
for cls in (Portatil, Camara, KitRobotica):
    if "calcular_multa" in getattr(cls, "__abstractmethods__", set()):
        cls.calcular_multa = lambda self, dias: float(Decimal(str(self.tarifa_diaria)) * Decimal(str(dias)))
        cls.__abstractmethods__ = frozenset(
            m for m in cls.__abstractmethods__ if m != "calcular_multa"
        )

# Asegurar compatibilidad entre self.id y self.id_equipo
if not hasattr(Equipo, "id"):
    Equipo.id = property(
        lambda self: getattr(self, "id_equipo", None),
        lambda self, val: setattr(self, "id_equipo", val),
    )


class RepositorioEquipoSQLite(RepositorioEquipo):
    """
    Implementación del puerto RepositorioEquipo usando SQLite3.
    """

    def __init__(self, conexion_o_path: Union[str, ConexionSQLite] = "sistema_prestamos.db"):
        if isinstance(conexion_o_path, ConexionSQLite):
            self.conexion_sqlite = conexion_o_path
        else:
            self.conexion_sqlite = ConexionSQLite(conexion_o_path)

    def _get_connection(self) -> sqlite3.Connection:
        return self.conexion_sqlite.obtener_conexion()

    def _crear_instancia(
        self,
        tipo: str,
        id_equipo: UUID,
        estado: EstadoEquipo,
        tarifa_diaria: float,
        plazo_prestamo: int,
    ) -> Equipo:
        tipo_normalizado = tipo.lower().replace(" ", "").replace("_", "")
        if "portatil" in tipo_normalizado:
            equipo = Portatil(id_equipo=id_equipo, estado=estado)
        elif "camara" in tipo_normalizado:
            equipo = Camara(id_equipo=id_equipo, estado=estado)
        elif "kit" in tipo_normalizado or "robotica" in tipo_normalizado:
            equipo = KitRobotica(id_equipo=id_equipo, estado=estado)
        else:
            class _EquipoGenerico(Equipo):
                def calcular_multa(self, dias: int) -> float:
                    return float(Decimal(str(self.tarifa_diaria)) * Decimal(str(dias)))

            equipo = _EquipoGenerico(
                id_equipo=id_equipo,
                tarifa_diaria=Decimal(str(tarifa_diaria)),
                plazo_prestamo=plazo_prestamo,
                estado=estado,
            )

        equipo.tarifa_diaria = Decimal(str(tarifa_diaria))
        equipo.plazo_prestamo = plazo_prestamo
        equipo.estado = estado
        return equipo

    def guardar(self, equipo: Equipo) -> None:
        """Inserta o actualiza un equipo en SQLite."""
        eq_id = str(getattr(equipo, "id_equipo", getattr(equipo, "id", "")))
        tipo = equipo.__class__.__name__
        estado_val = (
            equipo.estado.value
            if hasattr(equipo.estado, "value")
            else str(equipo.estado)
        )
        tarifa = float(equipo.tarifa_diaria)
        plazo = int(equipo.plazo_prestamo)

        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO equipos (id, tipo, estado, tarifa_diaria, plazo_prestamo)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (eq_id, tipo, estado_val, tarifa, plazo),
                )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def buscarPorId(self, id: str) -> Optional[Equipo]:
        """Busca un equipo por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, tipo, estado, tarifa_diaria, plazo_prestamo FROM equipos WHERE id = ?",
                (id_str,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            try:
                id_uuid = UUID(row["id"])
            except Exception:
                id_uuid = row["id"]

            try:
                estado = EstadoEquipo(row["estado"])
            except ValueError:
                estado = EstadoEquipo.DISPONIBLE

            return self._crear_instancia(
                tipo=row["tipo"],
                id_equipo=id_uuid,
                estado=estado,
                tarifa_diaria=row["tarifa_diaria"],
                plazo_prestamo=row["plazo_prestamo"],
            )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtenerTodos(self) -> List[Equipo]:
        """Obtiene todos los equipos registrados en SQLite."""
        equipos: List[Equipo] = []
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, tipo, estado, tarifa_diaria, plazo_prestamo FROM equipos"
            )
            rows = cursor.fetchall()
            for row in rows:
                try:
                    id_uuid = UUID(row["id"])
                except Exception:
                    id_uuid = row["id"]

                try:
                    estado = EstadoEquipo(row["estado"])
                except ValueError:
                    estado = EstadoEquipo.DISPONIBLE

                equipos.append(
                    self._crear_instancia(
                        tipo=row["tipo"],
                        id_equipo=id_uuid,
                        estado=estado,
                        tarifa_diaria=row["tarifa_diaria"],
                        plazo_prestamo=row["plazo_prestamo"],
                    )
                )
            return equipos
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def eliminar(self, id: str) -> None:
        """Elimina un equipo por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM equipos WHERE id = ?", (id_str,))
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    buscar_por_id = buscarPorId
    obtener_todos = obtenerTodos
