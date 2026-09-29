from decimal import Decimal

from aplicacion.puertos.Notificador import Notificador
from aplicacion.puertos.ProveedorFecha import ProveedorFecha
from aplicacion.puertos.RepositorioEquipo import RepositorioEquipo
from aplicacion.puertos.RepositorioMulta import RepositorioMulta
from aplicacion.puertos.RepositorioPrestamo import RepositorioPrestamo
from dominio.Enums import CondicionDevolucion, EstadoEquipo, EstadoMulta, EstadoPrestamo
from dominio.Excepciones import EntidadNoEncontradaError, PrestamoInvalidoError
from dominio.Multa import Multa


class RegistrarDevolucion:
    def __init__(
        self,
        repo_prestamo: RepositorioPrestamo,
        repo_equipo: RepositorioEquipo,
        repo_multa: RepositorioMulta,
        notificador: Notificador,
        fecha: ProveedorFecha,
    ):
        self.repo_prestamo = repo_prestamo
        self.repo_equipo = repo_equipo
        self.repo_multa = repo_multa
        self.notificador = notificador
        self.fecha = fecha

    def ejecutar(self, id_prestamo: str, condicion: CondicionDevolucion):
        prestamo = self.repo_prestamo.buscar_por_id(id_prestamo)
        if prestamo is None:
            raise EntidadNoEncontradaError("Préstamo no existe.")
        if prestamo.estado != EstadoPrestamo.ACTIVO:
            raise PrestamoInvalidoError("El préstamo ya fue finalizado.")

        dias, total = prestamo.finalizar(self.fecha.hoy())
        prestamo.equipo.estado = self._estado_equipo(condicion)
        self.repo_equipo.guardar(prestamo.equipo)
        self.repo_prestamo.guardar(prestamo)
        multa = self._crear_multa(prestamo, total)
        if multa is not None:
            self.repo_multa.guardar(multa)
            self._notificar_multa(prestamo, total)
        return prestamo, dias, total

    def _estado_equipo(self, condicion: CondicionDevolucion) -> EstadoEquipo:
        if condicion == CondicionDevolucion.DANADO:
            return EstadoEquipo.EN_MANTENIMIENTO
        return EstadoEquipo.DISPONIBLE

    def _crear_multa(self, prestamo, total: Decimal):
        if total <= Decimal("0"):
            return None
        return Multa(
            id_multa=f"multa-{prestamo.id}",
            tarifa=prestamo.tarifa_pactada,
            total=total,
            estado=EstadoMulta.PENDIENTE,
            estudiante_id=prestamo.estudiante.id,
        )

    def _notificar_multa(self, prestamo, total: Decimal) -> None:
        self.notificador.notificar_devolucion_multa(
            prestamo.estudiante.nombre,
            total,
            prestamo.equipo.__class__.__name__,
            prestamo.estudiante.correo,
        )
