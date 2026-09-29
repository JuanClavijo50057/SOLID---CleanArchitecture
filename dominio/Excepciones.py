class DominioError(Exception):
    pass

class EntidadNoEncontradaError(DominioError):
    pass

class EquipoNoDisponibleError(DominioError):
    pass

class PrestamoInvalidoError(DominioError):
    pass

class LimitePrestamosError(DominioError): 
    pass   

class MultaPendienteError(DominioError): 
    pass