from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import re
from datetime import datetime
from Mensaje import Mensaje
from Servicio import Servicio

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
    total_sentimientos = 0

    lista_positivo = []
    lista_negativo = []
    lista_mensaje = []
    lista_empresa = []
    lista_servicio = []
    lista_alias = []
    lista_resultado = []
    lista_ali = []
    listado_empresas = []

    for dato in root.findall('./diccionario/empresas_analizar/empresa/nombre'): 
        
        empresa = dato.text
        lista_empresa.append(empresa)

    for dato in root.findall('./diccionario/empresas_analizar/empresa/servicio'): 
        
        servicio = dato.get('nombre')
    
        for a in dato.findall('./alias'):
            alias = a.text
            lista_ali.append(alias)
            lista_alias.append(alias)

        lista_servicio.append(Servicio(servicio, lista_ali))
        lista_ali = []

    
    for i in range(len(lista_servicio)):

        print("\nel nombre del servicio: ",lista_servicio[i].getNombre(), " la lista de servicio ", lista_servicio[i].getListaServicio())
    print()

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
        
        
    
    #print(lista_positivo)
    #print(lista_negativo)
    #print(lista_mensaje)
    #print(lista_empresa)
    #print(lista_servicio)
    #print(lista_alias)

    response = []

    print("********MENSAJES ENCONTRADOS*********")
    
    
    for lista in range(len(lista_mensaje)):
        
        for empresa in lista_empresa:
            
            print("*******************ITERACION FOR DE EMPRESA ***************************")
            print("                     ", empresa, "                 ", str(lista), "     ")
            
            x = re.findall(empresa, lista_mensaje[lista], flags=re.IGNORECASE)
        
            print("esta es la lista ",x)

            if len(x) != 0 : # si la lista x no esta vacia
                if len(lista_resultado) == 0:
                    lista_resultado.append(Mensaje(empresa,0,0,0,0,""))
                    print("se guardo la empresa ", empresa)
                else:
                    existe_empresa = 0
                    for m in lista_resultado:
                        if m.getNombre() == empresa:
                            print("Ya existe", empresa , "en la lista resultado")
                            existe_empresa +=1
                    
                    if existe_empresa == 0 :
                        lista_resultado.append(Mensaje(empresa,0,0,0,0,""))
                        print("se guardo la empresa ", empresa)

                for palabra in lista_positivo:
                    x = re.findall(palabra, lista_mensaje[lista], flags=re.IGNORECASE)   # devuelve una lista con la palabra encontrada
            
                    if len(x) != 0:
                        contador_positivo +=1

                        for f in range(len(lista_resultado)):
                            if lista_resultado[f].getNombre() == empresa:
                                cont = lista_resultado[f].getPositivos() + contador_positivo
                                lista_resultado[f].setPositivos(cont)
                                contador_positivo = 0

                    response.append({palabra: len(x)})
                print()

                for palabra in lista_negativo:
                    x = re.findall(palabra, lista_mensaje[lista], flags=re.IGNORECASE)
            
                    if len(x) != 0:
                        contador_negativo +=1

                        for f in range(len(lista_resultado)):
                            if lista_resultado[f].getNombre() == empresa:
                                cont = lista_resultado[f].getNegativos() + contador_negativo
                                lista_resultado[f].setNegativos(cont)
                                contador_negativo = 0
                
                print(" EL LISTADO DE ALIAS ES ", lista_alias)
                for alias in lista_alias:
                    x = re.findall(alias, lista_mensaje[lista], flags=re.IGNORECASE)
                    
                    if len(x) != 0:
                        print("EL ALIAS ES ", alias)
                        for f in range(len(lista_resultado)):
                            if lista_resultado[f].getNombre() == empresa:
                                print("lista_resultado[f].getNombre()", lista_resultado[f].getNombre())
                                for h in range(len(lista_servicio)):
                                    for j in range(len(lista_servicio[h].getListaServicio())):
                                        if lista_servicio[h].getListaServicio()[j] == alias:
                                            print("if lista_servicio[h].getListaServicio()[j] == alias", lista_servicio[h].getListaServicio()[j])
                                            lista_resultado[f].setServicio(lista_servicio[h])
                            

    for f in range(len(lista_resultado)):

        if lista_resultado[f].getPositivos() == lista_resultado[f].getNegativos():
            contador_neutro += 1

        lista_resultado[f].setNeutros(contador_neutro)

        total_sentimientos = total_sentimientos+ lista_resultado[f].getPositivos() + lista_resultado[f].getNegativos() + contador_neutro

    #date_all = re.findall(r"(\d+/\d+/\d+)", lista_mensaje[lista])
    #print(date_all)  

    for f in range(len(lista_resultado)):

        print("nombre: ", lista_resultado[f].getNombre(), " positivos: ", str(lista_resultado[f].getPositivos()) 
        + " negativos: ", str(lista_resultado[f].getNegativos())," neutros: ", str(lista_resultado[f].getNeutros())
        + " servicio: ", lista_resultado[f].getServicio().getListaServicio() )

    print("TOTAL DE SENTIMIENTOS ", total_sentimientos)
    print("CONTADOR NEUTRO ", contador_neutro)

    return {'data': 'hola mundo'}
