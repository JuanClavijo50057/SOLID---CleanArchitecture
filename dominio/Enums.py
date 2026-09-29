from enum import Enum

class EstadoEquipo(Enum):
    DISPONIBLE = "Disponible"
    PRESTADO = "Prestado"
    EN_MANTENIMIENTO = "Mantenimiento"
    EXTRAVIADO = "Extraviado"

class EstadoPrestamo(Enum):
    ACTIVO = "Activo"
    FINALIZADO = "Finalizado"

class EstadoMulta(Enum):
    PENDIENTE = "Pendiente"
    PAGADA = "Pagada"

class CondicionDevolucion(Enum):
    BUEN_ESTADO = "BUEN_ESTADO"
    DANADO = "DANADO"