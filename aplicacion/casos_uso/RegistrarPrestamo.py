from uuid import UUID
from dominio.Prestamo import Prestamo
from dominio.Enums import EstadoEquipo
from dominio.Excepciones import (
    EntidadNoEncontradaError, EquipoNoDisponibleError, 
    LimitePrestamosError, MultaPendienteError
)
from aplicacion.puertos.RepositorioEstudiante import RepositorioEstudiante
from aplicacion.puertos.RepositorioEquipo import RepositorioEquipo
from aplicacion.puertos.RepositorioPrestamo import RepositorioPrestamo
from aplicacion.puertos.ProveedorFecha import ProveedorFecha
from aplicacion.puertos.Notificador import Notificador
from aplicacion.puertos.RepositorioMulta import RepositorioMulta

class RegistrarPrestamo:
    def __init__(self, repo_estud: RepositorioEstudiante, repo_eq: RepositorioEquipo, repo_prest: RepositorioPrestamo, repo_multa: RepositorioMulta, notificador: Notificador, fecha: ProveedorFecha):
        self.repo_estud = repo_estud
        self.repo_eq = repo_eq
        self.repo_prest = repo_prest
        self.repo_multa = repo_multa
        self.fecha = fecha
        self.notificador = notificador

    def ejecutar(self, id_prestamo: UUID, id_estudiante: UUID, id_equipo: UUID) -> Prestamo:
        estudiante = self._validar_reglas_estudiante(id_estudiante)
        equipo = self._obtener_equipo_disponible(id_equipo)         
        
        prestamo = Prestamo(id_prestamo, equipo, estudiante, self.fecha.hoy())
        equipo.estado = EstadoEquipo.PRESTADO
        
        self._persistir_transaccion(prestamo, equipo)
        self._notificar_exito(prestamo)
        return prestamo
    
    def _validar_reglas_estudiante(self, id_est: UUID):
        estudiante = self.repo_est.buscar_por_id(id_est)
        if not estudiante:
            raise EntidadNoEncontradaError("Estudiante no existe.")
            
        if len(self.repo_prest.obtener_activos_por_estudiante(id_est)) >= 2:
            raise LimitePrestamosError("R1: El estudiante ya tiene 2 préstamos activos.")
            
        if self.repo_multa.tiene_multas_pendientes(id_est):
            raise MultaPendienteError("R4: El estudiante tiene multas sin pagar.")
            
        return estudiante

    def _obtener_equipo_disponible(self, id_equipo: UUID):
        equipo = self.repo_eq.buscar_por_id(id_equipo)
        if not equipo or equipo.estado != EstadoEquipo.DISPONIBLE:
            raise EquipoNoDisponibleError("R2: El equipo no está DISPONIBLE.")
        return equipo

    def _persistir_transaccion(self, prestamo, equipo):
        self.repo_eq.guardar(equipo)
        self.repo_prest.guardar(prestamo)

    def _notificar_exito(self, prestamo):
        msj = f"Préstamo aprobado. R7: Fecha límite de entrega: {prestamo.fecha_limite}"
        self.notificador.enviar(prestamo.estudiante.correo, msj)