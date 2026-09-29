from uuid import UUID
from decimal import Decimal
from dominio.Enums import EstadoMulta

class Multa:
    def __init__(
        self, 
        id_multa: UUID, 
        tarifa: Decimal, 
        total: Decimal, 
        estado: EstadoMulta = EstadoMulta.PENDIENTE
    ):
        self.id = id_multa
        self.tarifa = tarifa
        self.total = total
        self.estado = estado

    def marcar_como_pagada(self) -> None:
        self.estado = EstadoMulta.PAGADA