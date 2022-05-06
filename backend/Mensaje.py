class Mensaje:
    def __init__(self, nombre_empresa, positivos, negativos, neutros, total, servicio, fecha, total_positivos, total_negativos):
        self.nombre_empresa = nombre_empresa
        self.positivos = positivos
        self.negativos = negativos
        self.neutros = neutros
        self.total = total
        self.servicio = servicio
        self.fecha = fecha
        self.total_positivos = total_positivos
        self.total_negativos = total_negativos

    def getNombre(self):
        return self.nombre_empresa

    def getPositivos(self):
        return self.positivos
    
    def getNegativos(self):
        return self.negativos

    def getNeutros(self):
        return self.neutros

    def getTotal(self):
        return self.total

    def getTotalPositivos(self):
        return self.total_positivos

    def getTotalNegativos(self):
        return self.total_negativos
    
    def getServicio(self):
        return self.servicio

    def getFecha(self):
        return self.fecha

    def setPositivos(self, positivos):
        self.positivos = positivos
    
    def setNegativos(self, negativos):
        self.negativos = negativos

    def setNeutros(self, neutros):
        self.neutros = neutros

    def setTotal(self, total):
        self.total = total

    def setTotalPositivos(self, total):
        self.total_positivos = total

    def setTotalNegativos(self, total):
        self.total_negativos = total
    
    def setServicio(self, servicio):
        self.servicio = servicio
    
    def setNombre(self, nombre_empresa):
        self.nombre_empresa = nombre_empresa
    
    def setFecha(self, fecha):
        self.fecha = fecha