from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import re
from datetime import datetime
from Mensaje import Mensaje
from Empresa import Empresa

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def hola():
    #xmlfile = "C:\Users\Darkun\Desktop\Entrada_Ejemplo.xml"
    doc = ET.parse('C:\\Users\\Darkun\\Desktop\\Entrada_Ejemplo.xml') #xmlfile contiene la ruta del archivo y se procesa
    root = doc.getroot()
        
       
    for ciudad in root.findall('./listaCiudades/ciudad'):           
            
        nombre = ciudad.find('./nombre').text
        print("el nombre de la ciudad es: ", nombre)

    return jsonify({"nombre": nombre})

@app.route("/palabras", methods=["POST"])
def parseInfo():
    body = request.get_json()

    archivo = body["archivo"]
    root = ET.fromstring(archivo)

    prueba = 'hola mundo'
    f = open ('salida.xml','w')
    f.write(prueba)
    f.close()
    
    contador_positivo=0
    contador_negativo=0
    contador_neutro=0
    total_mensajes = 0

    lista_positivo = []
    lista_negativo = []
    lista_mensaje = []
    lista_empresa = []
    lista_servicio = []
    lista_alias = []
    lista_resultado = []

    listado_empresas = []

    for dato in root.findall('./diccionario/empresas_analizar/empresa/nombre'): 
        
        empresa = dato.text
        lista_empresa.append(empresa)

    for dato in root.findall('./diccionario/empresas_analizar/empresa/servicio'): 
        
        servicio = dato.get('nombre')
        lista_servicio.append(servicio)

    for dato in root.findall('./diccionario/empresas_analizar/empresa/servicio/alias'): 
        
        alias = dato.text
        lista_alias.append(alias)

    for dato in root.findall('./diccionario/sentimientos_positivos/palabra'): 
        
        nombre = dato.text
        lista_positivo.append(nombre)

    for dato in root.findall('./diccionario/sentimientos_negativos/palabra'): 
        
        nombre = dato.text        
        lista_negativo.append(nombre)

    for dato in root.findall('./lista_mensajes/mensaje'): 
        
        mensaje = dato.text 

        indice_c = mensaje.index('Red social')
        sub = mensaje[indice_c:]
        lista_mensaje.append(sub)
        
        
    
    print(lista_positivo)
    print(lista_negativo)
    print(lista_mensaje)
    print(lista_empresa)
    print(lista_servicio)
    print(lista_alias)

    response = []

    print("********************ANALIZANDO LISTAS***********************")
    lista_prueba = ['USAC']
    lista_prueba = ['Landivar']
    print("esta es la lista de pruebas",lista_prueba)

    print("********MENSAJES ENCONTRADOS*********")
    
    for lista in range(len(lista_mensaje)):
        
        for empresa in lista_empresa:
            
            x = re.findall(empresa, lista_mensaje[lista], flags=re.IGNORECASE)
        
            print("esta es la lista ",x)
            #print("empresa ", empresa, " lista mensaje ", lista_mensaje[lista])

            if len(x) != 0 : # si la lista x no esta vacia
                lista_resultado.append(Mensaje(empresa,0,0,0,0,""))
                print("se guardo la empresa ", empresa)

            for palabra in lista_positivo:
                x = re.findall(palabra, lista_mensaje[lista], flags=re.IGNORECASE)   # devuelve una lista con la palabra encontrada
            
                if len(x) != 0:
                    contador_positivo +=1

                response.append({palabra: len(x)})
        
            print()

            for palabra in lista_negativo:
                x = re.findall(palabra, lista_mensaje[lista], flags=re.IGNORECASE)
            
                if len(x) != 0:
                    contador_negativo +=1
            
            print()

            for f in range(len(lista_resultado)):
                if lista_resultado[f].getNombre() == empresa:
                    lista_resultado[f].setPositivos(contador_positivo)
                    lista_resultado[f].setNegativos(contador_negativo)
                    print("nombre: ", lista_resultado[f].getNombre(), " positivos: ", lista_resultado[f].getPositivos(), " negativos: ", lista_resultado[f].getNegativos())

        '''
        for servicio in lista_servicio:
            x = re.findall(servicio, lista_mensaje[lista], flags=re.IGNORECASE)
            
            if len(x) != 0 : # si la lista x no esta vacia
                for a in lista_resultado:
                    a.setServicio(servicio)

        for alias in lista_alias:
            x = re.findall(alias, lista_mensaje[lista], flags=re.IGNORECASE)
        '''

    if contador_negativo == contador_positivo:
        contador_neutro += 1

    total_mensajes = contador_positivo + contador_negativo + contador_neutro

    #date_all = re.findall(r"(\d+/\d+/\d+)", lista_mensaje[lista])
    #print(date_all)  

        
    #print("El total de sentimientos recibidos es ", total_mensajes)
    #print("El valor de contador positivo es ", contador_positivo)
    #print("El valor de contador negativo es ", contador_negativo)
    
    #for i in lista_resultado:
        #print("nombre: ", i.getNombre(), "total positivos: ", str(i.getPositivos()), " total negativos: ", str(i.getNegativos()))

    '''
    for i in lista_resultado:
        for a in lista_empresa:
            if i.getNombre() == lista_empresa[a]:
                listado_empresas.append(Empresa(i.getNombre()))
    '''
    return {'data': 'hola mundo'}
