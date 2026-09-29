from datetime import date, timedelta
from decimal import Decimal

from dominio.Prestable import Prestable
from dominio.Equipo import Equipo
from dominio.Enums import EstadoPrestamo

class Prestamo(Prestable):
    def __init__(
        self,
        id_prestamo: str,
        equipo: Equipo,
        estudiante,
        fecha_inicial: date,
        fecha_limite: date = None,
        estado: EstadoPrestamo = EstadoPrestamo.ACTIVO
    ):
        self.id = str(id_prestamo)
        self.equipo = equipo
        self.estudiante = estudiante
        self.estudiante_id = estudiante.id
        self.fecha_inicial = fecha_inicial
        self.estado = estado

        self.fecha_limite = fecha_limite or fecha_inicial + timedelta(days=equipo.plazo_prestamo)
        
        # Tarifa histórica congelada
        self.tarifa_pactada: Decimal = equipo.tarifa_diaria
        # self.multa: Optional[Multa] = None

    def calcular_dias_retraso(self, fecha_devolucion: date) -> int:
        dias = (fecha_devolucion - self.fecha_limite).days
        return dias if dias > 0 else 0

    def calcular_multa(self, dias_retraso: int) -> Decimal:
        if dias_retraso <= 0:
            return Decimal('0.00')
        return Decimal(dias_retraso) * self.tarifa_pactada

    def finalizar(self, fecha_devolucion: date):
        self.estado = EstadoPrestamo.FINALIZADO
        
        dias_retraso = self.calcular_dias_retraso(fecha_devolucion)
        total_pagar = self.calcular_multa(dias_retraso)
        
        return dias_retraso, total_pagar