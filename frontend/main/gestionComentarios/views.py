from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#IMPORTANTE CREAR CARPETA template Y dentro crear otra carpeta con el mismo nombre del proyecto gestionComentarios

def saludo(request):
    return render(request, "gestionComentarios/Empresa.html", {"nombre": 'Tecnologias Chapinas'})