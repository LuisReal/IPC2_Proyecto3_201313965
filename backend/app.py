from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])

def hola():
    return jsonify([{'name': 'Tabletas', 'price': 10.88}, {'name': 'Curitas', 'price': 12.11}])