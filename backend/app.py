from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def hola():
    return jsonify([{'name': 'Tabletas', 'price': 10.88}, {'name': 'Curitas', 'price': 12.11}])

@app.route("/palabras", methods=["POST"])
def parseInfo():
    body = request.get_json()

    archivo = body["archivo"]
    
    for dato in archivo.findall('./diccionario/sentimientos_positivos'): 
        
        nombre = dato.find('./palabra').text
        print("el nombre de la ciudad es: ", nombre)

    return {'data': 'esta es la respuesta'}
