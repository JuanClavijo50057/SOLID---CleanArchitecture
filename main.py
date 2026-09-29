from datetime import date
from decimal import Decimal

from aplicacion.casos_uso.RegistrarDevolucion import RegistrarDevolucion
from aplicacion.casos_uso.RegistrarPrestamo import RegistrarPrestamo
from dominio.Camara import Camara
from dominio.Enums import CondicionDevolucion, EstadoEquipo, EstadoMulta
from dominio.Estudiante import Estudiante
from dominio.Excepciones import DominioError
from dominio.KitRobotica import KitRobotica
from dominio.Proyector import Proyector
from dominio.Multa import Multa
from dominio.Portatil import Portatil
from dominio.Prestamo import Prestamo
from infraestructura.ConexionSQLite import ConexionSQLite
from infraestructura.NotificadorGmail import NotificadorGmail
from infraestructura.ProveedorFechaFija import ProveedorFechaFija
from infraestructura.RepositorioEquipoSQLite import RepositorioEquipoSQLite
from infraestructura.RepositorioEstudianteSQLite import RepositorioEstudianteSQLite
from infraestructura.RepositorioMultaSQLite import RepositorioMultaSQLite
from infraestructura.RepositorioPrestamoSQLite import RepositorioPrestamoSQLite


def demo():
	fecha = ProveedorFechaFija(date(2026, 10, 5))
	conexion = ConexionSQLite("sistema_prestamos.db")
	_limpiar_datos_demo(conexion)
	estudiantes = RepositorioEstudianteSQLite(conexion)
	creadores_equipo = {
		"Portatil": Portatil,
		"Camara": Camara,
		"KitRobotica": KitRobotica,
		"Proyector": Proyector,
	}
	equipos = RepositorioEquipoSQLite(conexion, creadores_equipo)
	prestamos = RepositorioPrestamoSQLite(conexion, equipos, estudiantes)
	multas = RepositorioMultaSQLite(conexion)
	notificador = NotificadorGmail()
	registrar_devolucion = RegistrarDevolucion(
		prestamos, equipos, multas, notificador, fecha
	)
	registrar = RegistrarPrestamo(
		estudiantes, equipos, prestamos, multas, notificador, fecha
	)

	ana = Estudiante("ana", "Ana", "001", "ana@laboratorio.edu")
	luis = Estudiante("luis", "Luis", "002", "luis@laboratorio.edu")
	carlos = Estudiante("carlos", "Carlos", "003", "carlos@laboratorio.edu")
	sofia = Estudiante("sofia", "Sofia", "004", "sofia@laboratorio.edu")
	for estudiante in (ana, luis, carlos, sofia):
		estudiantes.guardar(estudiante)

	portatil = Portatil("PORTATIL-01")
	portatil_extra = Portatil("PORTATIL-03")
	camara = Camara("CAMARA-02")
	equipos.guardar(portatil)
	equipos.guardar(portatil_extra)
	equipos.guardar(camara)

	print("CA1")
	prestamo_ana = registrar.ejecutar("prestamo-ana", "ana", "PORTATIL-01")
	print(prestamo_ana.fecha_limite)

	print("CA2")
	registrar.ejecutar("prestamo-ana-2", "ana", "PORTATIL-03")
	try:
		registrar.ejecutar("prestamo-ana-3", "ana", "CAMARA-02")
	except DominioError as error:
		print(error)

	equipos.buscar_por_id("CAMARA-02").estado = EstadoEquipo.DISPONIBLE
	equipos.guardar(equipos.buscar_por_id("CAMARA-02"))
	prestamo_camara = Prestamo(
		"prestamo-camara", camara, carlos, date(2026, 10, 1)
	)
	equipos.buscar_por_id("CAMARA-02").estado = EstadoEquipo.PRESTADO
	equipos.guardar(equipos.buscar_por_id("CAMARA-02"))
	prestamos.guardar(prestamo_camara)

	print("CA3")
	fecha.fecha = date(2026, 10, 6)
	_, dias, total = registrar_devolucion.ejecutar(
		"prestamo-camara", CondicionDevolucion.BUEN_ESTADO
	)
	print(f"{dias} dias, ${total}")

	print("CA4")
	multas.guardar(Multa("multa-luis", Decimal("5000"), Decimal("5000"), estudiante_id="luis"))
	try:
		registrar.ejecutar("prestamo-luis", "luis", "CAMARA-02")
	except DominioError as error:
		print(error)

	print("CA5")
	registrar.ejecutar("prestamo-danado", "sofia", "CAMARA-02")
	fecha.fecha = date(2026, 10, 5)
	registrar_devolucion.ejecutar(
		"prestamo-danado", CondicionDevolucion.DANADO
	)
	print(equipos.buscar_por_id("CAMARA-02").estado.name)


def _limpiar_datos_demo(conexion):
	conn = conexion.obtener_conexion()
	with conn:
		for tabla in ("notificaciones", "multas", "prestamos", "equipos", "estudiantes"):
			conn.execute(f"DELETE FROM {tabla}")
	if conexion._memory_conn is None:
		conn.close()


if __name__ == "__main__":
	demo()
