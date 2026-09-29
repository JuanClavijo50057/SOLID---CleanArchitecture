import sqlite3
from typing import Callable, Dict, List, Union

from aplicacion.puertos.RepositorioEquipo import RepositorioEquipo
from infraestructura.ConexionSQLite import ConexionSQLite
from dominio.Equipo import Equipo
from dominio.Enums import EstadoEquipo
from dominio.Portatil import Portatil
from dominio.Camara import Camara
from dominio.KitRobotica import KitRobotica


class RepositorioEquipoSQLite(RepositorioEquipo):
    """
    Implementación del puerto RepositorioEquipo usando SQLite3.
    """

    def __init__(
        self,
        conexion_o_path: Union[str, ConexionSQLite] = "sistema_prestamos.db",
        creadores: Dict[str, Callable] = None,
    ):
        if isinstance(conexion_o_path, ConexionSQLite):
            self.conexion_sqlite = conexion_o_path
        else:
            self.conexion_sqlite = ConexionSQLite(conexion_o_path)
        self.creadores = creadores or {
            "Portatil": Portatil,
            "Camara": Camara,
            "KitRobotica": KitRobotica,
        }

    def _get_connection(self) -> sqlite3.Connection:
        return self.conexion_sqlite.obtener_conexion()

    def _crear_instancia(self, tipo: str, id_equipo: str, estado: EstadoEquipo) -> Equipo:
        creador = self.creadores.get(tipo)
        if creador is None:
            raise ValueError(f"Tipo de equipo desconocido: {tipo}")
        return creador(id_equipo=id_equipo, estado=estado)

    def guardar(self, equipo: Equipo) -> None:
        """Inserta o actualiza un equipo en SQLite."""
        eq_id = str(getattr(equipo, "id_equipo", getattr(equipo, "id", "")))
        tipo = equipo.__class__.__name__
        estado_val = (
            equipo.estado.value
            if hasattr(equipo.estado, "value")
            else str(equipo.estado)
        )

        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO equipos (id, tipo, estado)
                    VALUES (?, ?, ?)
                    """,
                    (eq_id, tipo, estado_val),
                )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def buscar_por_id(self, id: str) -> Equipo:
        """Busca un equipo por ID en SQLite."""
        id_str = str(id)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, tipo, estado FROM equipos WHERE id = ?",
                (id_str,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            estado_raw = row["estado"]
            try:
                estado = EstadoEquipo(estado_raw)
            except ValueError:
                try:
                    estado = EstadoEquipo[estado_raw]
                except KeyError:
                    estado = EstadoEquipo.DISPONIBLE

            return self._crear_instancia(
                tipo=row["tipo"],
                id_equipo=str(row["id"]),
                estado=estado,
            )
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def buscarPorId(self, id: str) -> Equipo:
        """Alias para cumplir con la interfaz del puerto RepositorioEquipo."""
        return self.buscar_por_id(id)

    def obtener_todos(self) -> List[Equipo]:
        """Obtiene todos los equipos registrados en SQLite."""
        equipos: List[Equipo] = []
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, tipo, estado FROM equipos")
            rows = cursor.fetchall()
            for row in rows:
                estado_raw = row["estado"]
                try:
                    estado = EstadoEquipo(estado_raw)
                except ValueError:
                    try:
                        estado = EstadoEquipo[estado_raw]
                    except KeyError:
                        estado = EstadoEquipo.DISPONIBLE

                equipos.append(
                    self._crear_instancia(
                        tipo=row["tipo"],
                        id_equipo=str(row["id"]),
                        estado=estado,
                    )
                )
            return equipos
        finally:
            if self.conexion_sqlite._memory_conn is None:
                conn.close()

    def obtenerTodos(self) -> List[Equipo]:
        """Alias para cumplir con la interfaz del puerto RepositorioEquipo."""
        return self.obtener_todos()

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
