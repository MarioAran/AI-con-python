from flask import Flask, jsonify, request as req

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>this is s test </h1> <p>Hello, World!</p>"

@app.route("/saludar/<nombre>", methods = ["GET"])
def saludar(nombre):
    return jsonify({"about": "Hola "+nombre+"!"})

@app.route("/guardar/", methods = ["POST"])
def guardar():
    nombre = req.form["user"]
    apellido = req.form["passwd"]
    return jsonify({"about": "Hola "+nombre+" "+apellido})