class Servicio:
    def __init__(self, nombre, lista):
        self.nombre = nombre
        self.lista_servicio = lista
        
    
    def getNombre(self):
        return self.nombre
    
    def getListaServicio(self):
        return self.lista_servicio

    def setNombre(self, nombre):
        self.nombre = nombre
    
    def setListaServicio(self, lista):
        self.lista_servicio = lista

    