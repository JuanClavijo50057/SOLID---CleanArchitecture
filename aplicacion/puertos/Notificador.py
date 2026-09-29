from abc import ABC, abstractmethod
from decimal import Decimal

class Notificador(ABC):
    """
    Puerto (Interfaz) para el servicio de notificaciones.
    Define las operaciones para enviar notificaciones a los estudiantes.
    """

    @abstractmethod
    def notificar_prestamo(
        self,
        estudiante_nombre: str,
        equipo_nombre: str,
        fecha_limite: str,
        correo: str
    ) -> None:
        """Notifica al estudiante sobre un préstamo registrado."""
        pass

    @abstractmethod
    def notificar_devolucion_multa(
        self,
        estudiante_nombre: str,
        monto_multa: Decimal,
        nombre_equipo: str,
        correo: str
    ) -> None:
        """Notifica al estudiante sobre una multa generada en la devolución."""
        pass