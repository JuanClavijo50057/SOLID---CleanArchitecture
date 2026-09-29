from datetime import date
from aplicacion.puertos.ProveedorFecha import ProveedorFecha


class ProveedorFechaFija(ProveedorFecha):
    def __init__(self, fecha: date):
        self.fecha = fecha

    def hoy(self) -> date:
        return self.fecha
