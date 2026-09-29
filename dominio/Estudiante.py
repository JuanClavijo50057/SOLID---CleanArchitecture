from uuid import UUID

class Estudiante:
    def __init__(self, id_estudiante: UUID, nombre: str, codigo: str, correo: str):
        self.id = id_estudiante
        self.nombre = nombre
        self.codigo = codigo
        self.correo = correo