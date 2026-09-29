from decimal import Decimal
from typing import List, Dict, Any
from aplicacion.puertos.Notificador import Notificador


class NotificadorGmail(Notificador):
    """
    Adaptador simulado de notificaciones por correo (Gmail).
    Implementa el puerto Notificador.
    """

    def __init__(self):
        self.notificaciones_enviadas: List[Dict[str, Any]] = []

    def notificar_prestamo(
        self,
        estudiante_nombre: str,
        equipo_nombre: str,
        fecha_limite: str,
        correo: str,
    ) -> None:
        """Simula el envío de correo de confirmación de préstamo."""
        mensaje = (
            f"[GMAIL SIMULADO] Para: {correo} | Estimado(a) {estudiante_nombre}, "
            f"se ha registrado el préstamo del equipo '{equipo_nombre}'. "
            f"Fecha límite de devolución: {fecha_limite}."
        )
        print(mensaje)
        self.notificaciones_enviadas.append(
            {
                "tipo": "prestamo",
                "correo": correo,
                "estudiante": estudiante_nombre,
                "equipo": equipo_nombre,
                "fecha_limite": fecha_limite,
                "mensaje": mensaje,
            }
        )

    def notificar_devolucion_multa(
        self,
        estudiante_nombre: str,
        monto_multa: Decimal,
        nombre_equipo: str,
        correo: str,
    ) -> None:
        """Simula el envío de correo de notificación de multa por devolución tardía."""
        mensaje = (
            f"[GMAIL SIMULADO] Para: {correo} | Estimado(a) {estudiante_nombre}, "
            f"se registró la devolución del equipo '{nombre_equipo}'. "
            f"Se ha generado una multa de ${monto_multa} por retraso en la entrega."
        )
        print(mensaje)
        self.notificaciones_enviadas.append(
            {
                "tipo": "devolucion_multa",
                "correo": correo,
                "estudiante": estudiante_nombre,
                "equipo": nombre_equipo,
                "monto_multa": monto_multa,
                "mensaje": mensaje,
            }
        )
