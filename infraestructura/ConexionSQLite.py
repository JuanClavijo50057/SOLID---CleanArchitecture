import sqlite3
from typing import Optional


class ConexionSQLite:
    """
    Gestor de conexiones SQLite para la capa de infraestructura.
    Inicializa las tablas necesarias si no existen.
    """

    def __init__(self, db_path: str = "sistema_prestamos.db"):
        self.db_path = db_path
        self._memory_conn: Optional[sqlite3.Connection] = None
        if self.db_path == ":memory:":
            self._memory_conn = sqlite3.connect(":memory:")
            self._memory_conn.row_factory = sqlite3.Row
        self._inicializar_tablas()

    def obtener_conexion(self) -> sqlite3.Connection:
        """Retorna una conexión activa a la base de datos."""
        if self._memory_conn is not None:
            return self._memory_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _inicializar_tablas(self) -> None:
        """Crea las tablas de la base de datos si no existen."""
        conn = self.obtener_conexion()
        cursor = conn.cursor()

        # Tabla Estudiantes
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS estudiantes (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                codigo TEXT NOT NULL,
                correo TEXT NOT NULL
            );
            """
        )

        # Tabla Equipos: Persistencia limpia con solo id, tipo y estado
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS equipos (
                id TEXT PRIMARY KEY,
                tipo TEXT NOT NULL,
                estado TEXT NOT NULL
            );
            """
        )

        # Tabla Multas: Tarifas almacenadas como TEXT para precisión decimal exacta
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS multas (
                id TEXT PRIMARY KEY,
                estudiante_id TEXT NOT NULL,
                tarifa TEXT NOT NULL,
                total TEXT NOT NULL,
                estado TEXT NOT NULL
            );
            """
        )

        # Tabla Prestamos: Tarifa pactada como TEXT para precisión decimal exacta
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS prestamos (
                id TEXT PRIMARY KEY,
                estudiante_id TEXT NOT NULL,
                equipo_id TEXT NOT NULL,
                multa_id TEXT,
                tarifa_pactada TEXT NOT NULL,
                fecha_inicial TEXT NOT NULL,
                fecha_limite TEXT NOT NULL,
                estado TEXT NOT NULL
            );
            """
        )

        # Tabla Notificaciones
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notificaciones (
                id TEXT PRIMARY KEY,
                tipo TEXT,
                destinatario TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                fecha TEXT NOT NULL
            );
            """
        )

        conn.commit()
        if self._memory_conn is None:
            conn.close()
