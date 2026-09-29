from datetime import date
from aplicacion.puertos.ProveedorFecha import ProveedorFecha


class ProveedorFechaReal(ProveedorFecha):
    """
    Adaptador que provee la fecha real del sistema operativo.
    Implementa el puerto ProveedorFecha.
    """

    def hoy(self) -> date:
        return date.today()
