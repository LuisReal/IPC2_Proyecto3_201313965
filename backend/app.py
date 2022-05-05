from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import re

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
    
    contador_positivo=0
    contador_negativo=0
    contador_neutro=0
    total_mensajes = 0

    lista_positivo = []
    lista_negativo = []
    lista_mensaje = []

    for dato in root.findall('./diccionario/sentimientos_positivos/palabra'): 
        
        nombre = dato.text
        lista_positivo.append(nombre)

    for dato in root.findall('./diccionario/sentimientos_negativos/palabra'): 
        
        nombre = dato.text        
        lista_negativo.append(nombre)

    for dato in root.findall('./lista_mensajes/mensaje'): 
        
        mensaje = dato.text 
        lista_mensaje.append(mensaje)
    
    print(lista_positivo)
    print(lista_negativo)
    print(lista_mensaje)

    print("********MENSAJES POSITIVOS ENCONTRADOS*********")
    for palabra in lista_positivo:
        for lista in range(len(lista_mensaje)):
            x = re.findall("\\b("+palabra+")\\b", lista_mensaje[lista])   
            print(x)
            if len(x) != 0:
                contador_positivo +=1
            
    print("El valor de contador positivo es ", contador_positivo)
    print()
    print("********MENSAJES NEGATIVOS ENCONTRADOS*********")
    for palabra in lista_negativo:
        for lista in range(len(lista_mensaje)):
            x = re.findall("\\b("+palabra+")\\b", lista_mensaje[lista])
            print(x)
            if len(x) != 0:
                contador_negativo +=1

    print("El valor de contador negativo es ", contador_negativo)

    if contador_positivo == contador_negativo:
        print("EL MENSAJE ES NEUTRO")

    return {'data': 'esta es la respuesta'}
