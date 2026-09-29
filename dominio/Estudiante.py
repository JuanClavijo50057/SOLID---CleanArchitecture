class Estudiante:
    def __init__(self, id_estudiante: str, nombre: str, codigo: str, correo: str):
        self.id = str(id_estudiante)
        self.nombre = nombre
        self.codigo = codigo
        self.correo = correo