from decimal import Decimal
from dominio.Enums import EstadoMulta

class Multa:
    def __init__(
        self, 
        id_multa: str,
        tarifa: Decimal, 
        total: Decimal, 
        estado: EstadoMulta = EstadoMulta.PENDIENTE,
        estudiante_id: str = ""
    ):
        self.id = str(id_multa)
        self.tarifa = tarifa
        self.total = total
        self.estado = estado
        self.estudiante_id = str(estudiante_id)

    def marcar_como_pagada(self) -> None:
        self.estado = EstadoMulta.PAGADA