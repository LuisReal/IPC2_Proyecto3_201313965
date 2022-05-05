
import xml.etree.ElementTree as ET
from django.shortcuts import render
from django.http import HttpResponse
import requests as req
from django.template.defaultfilters import linebreaksbr
# Create your views here.
#IMPORTANTE CREAR CARPETA template Y dentro crear otra carpeta con el mismo nombre del proyecto gestionComentarios

def saludo(request):
    return render(request, "gestionComentarios/Empresa.html", {"nombre": 'Tecnologias Chapinas'})

def palabras(requests):

    result = ""
    text = ""
    datos =""
    file =""

    if requests.method == "POST": # recibe un metodo POST de la etiqueta en form en Empresa.html cuando se hace click al boton enviar
        text = requests.POST.get("textarea1")
        file = requests.FILES['file']

        result = text
        
        for chunk in file.chunks():
            datos = str(chunk)
        
        
        archivo = datos.replace('b\'<?xml version="1.0"?>', " ").replace('\'', ' ').replace("\\r\\n", "\r\n")
        
        root = ET.fromstring(archivo)
    
        for dato in root.findall('./diccionario/sentimientos_positivos'): 
            
            nombre = dato.find('./palabra').text
            print("el nombre del sentimiento positivo es: ", nombre)
        
        sendInfo(archivo)
    
    info = datos.replace("\\r\\n", "\r\n")

    context = {"result": result, "nombre": "Tecnologias Chapinas", "info": info} 
    return render(requests, "gestionComentarios/Empresa.html", context)

def sendInfo(archivo):
    data = {'archivo': archivo}

    response = req.post('http://127.0.0.1:5000/palabras', json=data) # se envia a la api de flask

