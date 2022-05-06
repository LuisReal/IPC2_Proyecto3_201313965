class Empresa:
    def __init__(self, nombre, positivos, negativos, neutros):
        self.nombre = nombre
        self.positivos = positivos
        self.negativos = negativos
        self.neutros = neutros
    
    def getNombre(self):
        return self.nombre
    
    def getPositivos(self):
        return self.positivos

    def getNegativos(self):
        return self.negativos
    
    def getNeutros(self):
        return self.neutros

    def setNombre(self, nombre):
        self.nombre = nombre
    
    def setPositivos(self, positivos):
        self.positivos = positivos

    def setNegativos(self, negativos):
        self.negativos = negativos
    
    def setNeutros(self, neutros):
        self.neutros = neutros
    