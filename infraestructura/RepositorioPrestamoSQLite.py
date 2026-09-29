import sqlite3
from typing import List, Union
from datetime import date
from decimal import Decimal

from aplicacion.puertos.RepositorioPrestamo import RepositorioPrestamo
from aplicacion.puertos.RepositorioEquipo import RepositorioEquipo
from infraestructura.ConexionSQLite import ConexionSQLite
from infraestructura.RepositorioEquipoSQLite import RepositorioEquipoSQLite
from dominio.Prestamo import Prestamo
from dominio.Enums import EstadoPrestamo, EstadoMulta


class RepositorioPrestamoSQLite(RepositorioPrestamo):
    """
    Implementación del puerto RepositorioPrestamo usando SQLite3.
    """

    def __init__(
        self,
        conexion_o_path: Union[str, ConexionSQLite] = "sistema_prestamos.db",
        repo_equipo: RepositorioEquipo = None,
    ):
        if isinstance(conexion_o_path, ConexionSQLite):
            self.conexion_sqlite = conexion_o_path
        else:
            self.conexion_sqlite = ConexionSQLite(conexion_o_path)

        self.repo_equipo = repo_equipo or RepositorioEquipoSQLite(self.conexion_sqlite)

    def _get_connection(self) -> sqlite3.Connection:
        return self.conexion_sqlite.obtener_conexion()

    def guardar(self, prestamo: Prestamo) -> None:
        """Inserta o actualiza un préstamo en SQLite."""
        p_id = str(prestamo.id)

        # Obtener estudiante_id
        estudiante = getattr(prestamo, "estudiante", None)
        estudiante_id = str(
            getattr(
                prestamo,
                "estudiante_id",
                getattr(estudiante, "id", getattr(estudiante, "id_estudiante", "")),
            ) or ""
        )

        # Obtener equipo_id
        equipo = getattr(prestamo, "equipo", None)
        eq_id = getattr(prestamo, "equipo_id", None)
        if not eq_id and equipo:
            eq_id = getattr(equipo, "id_equipo", getattr(equipo, "id", ""))
        equipo_id = str(eq_id or "")

        # Persistir equipo si es necesario
        if equipo and self.repo_equipo:
            equipo_existente = self.repo_equipo.buscar_por_id(equipo_id)
            if equipo_existente is None:
                self.repo_equipo.guardar(equipo)

        # Multa id opcional
        multa = getattr(prestamo, "multa", None)
        multa_id = getattr(prestamo, "multa_id", getattr(multa, "id", getattr(multa, "id_multa", None)))
        multa_id_str = str(multa_id) if multa_id else None

        # Precisión financiera: guardar como string del Decimal sin usar float
        tarifa_pactada_str = str(Decimal(str(prestamo.tarifa_pactada)))

        fecha_inicial = (
            prestamo.fecha_inicial.isoformat()
            if isinstance(prestamo.fecha_inicial, date)
            else str(prestamo.fecha_inicial)
        )
        fecha_limite = (
            prestamo.fecha_limite.isoformat()
            if isinstance(prestamo.fecha_limite, date)
            else str(prestamo.fecha_limite)
        )
        estado_val = (
            prestamo.estado.value
            if hasattr(prestamo.estado, "value")
            else str(prestamo.estado)
        )

        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO prestamos (
                        id, estudiante_id, equipo_id, multa_id,
                        tarifa_pactada, fecha_inicial, fecha_limite, estado
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        p_id,
                        estudiante_id,
                        equipo_id,
                        multa_id_str,
                        tarifa_pactada_str,
                        fecha_inicial,
                        fecha_limite,
                        estado_val,
                    ),
                )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def _reconstruir_prestamo(self, row: sqlite3.Row) -> Prestamo:
        equipo_id = row["equipo_id"]
        equipo = self.repo_equipo.buscar_por_id(equipo_id)
        if equipo is None:
            from dominio.Portatil import Portatil

            equipo = Portatil(id_equipo=str(equipo_id))

        fecha_ini = date.fromisoformat(row["fecha_inicial"])
        fecha_lim = date.fromisoformat(row["fecha_limite"])

        estado_raw = row["estado"]
        try:
            estado = EstadoPrestamo(estado_raw)
        except ValueError:
            try:
                estado = EstadoPrestamo[estado_raw]
            except KeyError:
                estado = EstadoPrestamo.ACTIVO

        prestamo = Prestamo(
            id_prestamo=str(row["id"]),
            equipo=equipo,
            fecha_inicial=fecha_ini,
            fecha_limite=fecha_lim,
            estado=estado,
        )
        prestamo.fecha_limite = fecha_lim
        # Precisión financiera: casteo explícito a Decimal instanciándolo desde string
        prestamo.tarifa_pactada = Decimal(str(row["tarifa_pactada"]))
        prestamo.estudiante_id = row["estudiante_id"]
        prestamo.equipo_id = row["equipo_id"]
        if "multa_id" in row.keys() and row["multa_id"]:
            prestamo.multa_id = row["multa_id"]
        return prestamo

    def buscar_por_id(self, id: str) -> Prestamo:
        """Busca un préstamo por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, estudiante_id, equipo_id, multa_id,
                       tarifa_pactada, fecha_inicial, fecha_limite, estado
                FROM prestamos
                WHERE id = ?
                """,
                (id_str,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return self._reconstruir_prestamo(row)
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def buscarPorId(self, id: str) -> Prestamo:
        """Alias para cumplir con la interfaz del puerto RepositorioPrestamo."""
        return self.buscar_por_id(id)

    def obtener_todos(self) -> List[Prestamo]:
        """Obtiene todos los préstamos registrados en SQLite."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, estudiante_id, equipo_id, multa_id,
                       tarifa_pactada, fecha_inicial, fecha_limite, estado
                FROM prestamos
                """
            )
            rows = cursor.fetchall()
            return [self._reconstruir_prestamo(row) for row in rows]
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtenerTodos(self) -> List[Prestamo]:
        """Alias para cumplir con la interfaz del puerto RepositorioPrestamo."""
        return self.obtener_todos()

    def eliminar(self, id: str) -> None:
        """Elimina un préstamo por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM prestamos WHERE id = ?", (id_str,))
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtener_activos_por_estudiante(self, id_estudiante: str) -> List[Prestamo]:
        """Retorna la lista de préstamos activos de un estudiante."""
        id_str = str(id_estudiante)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, estudiante_id, equipo_id, multa_id,
                       tarifa_pactada, fecha_inicial, fecha_limite, estado
                FROM prestamos
                WHERE estudiante_id = ? AND (estado = ? OR estado = ?)
                """,
                (id_str, EstadoPrestamo.ACTIVO.value, "ACTIVO"),
            )
            rows = cursor.fetchall()
            return [self._reconstruir_prestamo(row) for row in rows]
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def tiene_multas_pendientes(self, id_estudiante: str) -> bool:
        """Retorna True si el estudiante tiene al menos una multa pendiente."""
        id_str = str(id_estudiante)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 1 FROM prestamos p
                JOIN multas m ON p.multa_id = m.id
                WHERE p.estudiante_id = ? AND (m.estado = ? OR m.estado = ?)
                LIMIT 1
                """,
                (id_str, EstadoMulta.PENDIENTE.value, "PENDIENTE"),
            )
            return cursor.fetchone() is not None
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()
