class Notificacion:
    def __init__(
        self,
        id_notificacion: str,
        destinatario: str,
        mensaje: str,
        fecha: str,
        tipo: str = "general",
    ):
        self.id = str(id_notificacion)
        self.destinatario = destinatario
        self.mensaje = mensaje
        self.fecha = fecha
        self.tipo = tipo
