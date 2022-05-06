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
    total_positivos = 0
    total_negativos = 0

    lista_positivo = []
    lista_negativo = []
    lista_submensaje = []
    lista_empresa = []
    lista_servicio = []
    lista_alias = []
    lista_resultado = []
    lista_ali = []
    lista_mensajes = []
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

        lista_mensajes.append(mensaje)

        indice_c = mensaje.index('Red social')
        sub = mensaje[indice_c:]
        lista_submensaje.append(sub)
        
        
    
    #print(lista_positivo)
    #print(lista_negativo)
    #print(lista_mensaje)
    #print(lista_empresa)
    #print(lista_servicio)
    #print(lista_alias)

    response = []

    print("********MENSAJES ENCONTRADOS*********")
    
    
    for lista in range(len(lista_submensaje)):
        
        for empresa in lista_empresa:
            
            print("*******************ITERACION FOR DE EMPRESA ***************************")
            print("                     ", empresa, "                 ", str(lista), "     ")
            
            x = re.findall(empresa, lista_submensaje[lista], flags=re.IGNORECASE)
        
            print("esta es la lista ",x)

            if len(x) != 0 : # si la lista x no esta vacia
                if len(lista_resultado) == 0:
                    lista_resultado.append(Mensaje(empresa,0,0,0,0,"","",0,0))
                    print("se guardo la empresa ", empresa)
                else:
                    existe_empresa = 0
                    for m in lista_resultado:
                        if m.getNombre() == empresa:
                            print("Ya existe", empresa , "en la lista resultado")
                            existe_empresa +=1
                    
                    if existe_empresa == 0 :
                        lista_resultado.append(Mensaje(empresa,0,0,0,0,"", "",0,0))
                        print("se guardo la empresa ", empresa)

                for palabra in lista_positivo:
                    x = re.findall(palabra, lista_submensaje[lista], flags=re.IGNORECASE)   # devuelve una lista con la palabra encontrada
            
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
                    x = re.findall(palabra, lista_submensaje[lista], flags=re.IGNORECASE)
            
                    if len(x) != 0:
                        contador_negativo +=1

                        for f in range(len(lista_resultado)):
                            if lista_resultado[f].getNombre() == empresa:
                                cont = lista_resultado[f].getNegativos() + contador_negativo
                                lista_resultado[f].setNegativos(cont)
                                contador_negativo = 0
                
                print(" EL LISTADO DE ALIAS ES ", lista_alias)
                for alias in lista_alias:
                    x = re.findall(alias, lista_submensaje[lista], flags=re.IGNORECASE)
                    
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
           
                date_all = re.findall(r"(\d+/\d+/\d+)", lista_mensajes[lista])
                #print("la fecha es: ",date_all)

                for f in range(len(lista_resultado)):
                    if lista_resultado[f].getNombre() == empresa:
                        lista_resultado[f].setFecha(date_all)

    for f in range(len(lista_resultado)):

        if lista_resultado[f].getPositivos() == lista_resultado[f].getNegativos():
            contador_neutro += 1

        lista_resultado[f].setNeutros(contador_neutro)

        for k in range(len(lista_resultado)):
            if lista_resultado[f].getFecha()[0] == lista_resultado[k].getFecha()[0]:
                #print("lista_resultado[f].getFecha()[0]: ", lista_resultado[f].getFecha()[0])
                total_sentimientos = total_sentimientos+ lista_resultado[k].getPositivos() + lista_resultado[k].getNegativos() + contador_neutro
                total_positivos = total_positivos + lista_resultado[k].getPositivos() 
                total_negativos = total_negativos + lista_resultado[k].getNegativos()
                print("total de sentimientos iterando en el for ", total_sentimientos)
        
        lista_resultado[f].setTotal(total_sentimientos)
        lista_resultado[f].setTotalPositivos(total_positivos)
        lista_resultado[f].setTotalNegativos(total_negativos)

        print("total de sentimientos en 1 iteracion: ", total_sentimientos)
        total_sentimientos = 0  
        total_positivos = 0
        total_negativos = 0

    for f in range(len(lista_resultado)):

        print("nombre: ", lista_resultado[f].getNombre(), " positivos: ", str(lista_resultado[f].getPositivos()) 
        + " negativos: ", str(lista_resultado[f].getNegativos())," neutros: ", str(lista_resultado[f].getNeutros())
        + " servicio: ", lista_resultado[f].getServicio().getListaServicio(), " la fecha es: ", lista_resultado[f].getFecha(), " total mensajes: ",str(lista_resultado[f].getTotal()))
    #str(lista_resultado[f].getNegativos())
    print("TOTAL DE SENTIMIENTOS ", total_sentimientos)
    print("CONTADOR NEUTRO ", contador_neutro)

    xml = '''<lista_respuestas>
    <respuesta>
        <fecha>{{lista_resultado[0].getNombre()}}</fecha>'''

    f = open('Salida.xml','w')

    head = '<lista_respuestas>\n'
    body = ''
    fin = '</lista_respuestas>'

    for i in range(0,len(lista_resultado)):
        body += '   <respuesta>\n'
        body += '       <fecha>'
        body +=  lista_resultado[i].getFecha()[0]
        body += '</fecha>\n'
        body += '           <mensajes>\n'
        body += '           <total>'
        body +=  str(lista_resultado[i].getTotal())
        body += '</total>\n'
        body += '               <positivos>'
        body +=  str(lista_resultado[i].getTotalPositivos())
        body += '</positivos>\n'
        body += '               <negativos>'
        body +=  str(lista_resultado[i].getTotalNegativos())
        body += '</negativos>\n'
        body += '               <neutros>'
        body +=  str(lista_resultado[i].getNeutros())
        body += '</neutros>\n'
        body += '           </mensajes>\n'
        body += '       <analisis>\n'
        body += '           <empresa nombre = "'+lista_resultado[i].getNombre()+'">\n'
        body += '               <mensajes>\n'
        body += '               <total>'
        body +=  str(lista_resultado[i].getPositivos()+lista_resultado[i].getNegativos()+lista_resultado[i].getNeutros())
        body += '<total>\n'
        body += '               <positivos>'
        body += str(lista_resultado[i].getPositivos())
        body += '</positivos>\n'
        body += '               <negativos>'
        body += str(lista_resultado[i].getNegativos())
        body += '</negativos>\n'
        body += '               <neutros>'
        body += str(lista_resultado[i].getNeutros())
        body += '</neutros>\n'
        body += '               </mensajes>\n'
        body += '                   <servicios>\n'
        body += '                       <servicio nombre = "'+lista_resultado[i].getServicio().getNombre()+'">\n'
        body += '                           <mensajes>\n'
        body += '                               <total>'
        body += str(lista_resultado[i].getPositivos()+lista_resultado[i].getNegativos()+lista_resultado[i].getNeutros())
        body += '</total>\n'
        body += '                               <positivos>'
        body += str(lista_resultado[i].getPositivos())
        body += '</positivos>\n'
        body += '                               <negativos>'
        body += str(lista_resultado[i].getNegativos())
        body += '</negativos>\n'
        body += '                               <neutros>'
        body += '</neutros>\n'
        body += '                           </mensajes>\n'
        body += '                       </servicio>\n'
        body += '                   </servicios>\n'
        body += '           </empresa>\n'
        body += '       </analisis>\n'
        body += '   </respuesta>\n'
        

    cadena = head + body + fin

    f.write(cadena)
    f.close()

    r = open('Salida.xml','r')
    contenido = r.read()
    print(contenido)
    r.close()


    lista_datos = []

    for f in range(len(lista_resultado)):

        Dato={'Nombre' : lista_resultado[f].getNombre(),
            'Postivos': str(lista_resultado[f].getPositivos()),
            'Negativos': str(lista_resultado[f].getNegativos()),
            'Neutros': str(lista_resultado[f].getNeutros()),
            'Servicio:': lista_resultado[f].getServicio().getListaServicio(),
            'Fecha:': lista_resultado[f].getFecha(),
            'Total:' : str(lista_resultado[f].getTotal()) }  

        lista_datos.append(Dato)

    #contenido_txt = {'contenido': contenido}

    
    return {'data': contenido}
