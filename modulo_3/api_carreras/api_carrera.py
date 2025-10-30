import dao_Carrera as dao
from flask import Flask, jsonify, request
import carrera as c
import mysql.connector

app = Flask(__name__)

def connect_db():
    user = input("Introduce el usuario de la base de datos: ")
    passwd = input("Introduce la contraseña de la base de datos: ")
    cnx = dao.connect_db(user, passwd)
    return cnx

conexion = connect_db()
cursor = conexion.cursor(dictionary=True)

@app.route('/')
def hola_mundo():
    return '<p>Servidor Flask en ejecución correctamente.</p>'

@app.route('/ver/carreras/', methods=['GET'])
def api_ver_carreras():
    carreras_obj = dao.ver_carreras(cursor)
    carreras_dict = [carrera.to_dict() for carrera in carreras_obj]
    return jsonify(carreras_dict), 200



@app.route('/agregar/carrera/', methods=['POST'])
def api_agregar_carrera():
    error = ""
    data = request.get_json()
    nombre = data.get("nombre")
    nota = data.get("nota_corte")
    duracion = data.get("duracion")

    if not nombre:
        error +="error: Falta el nombre de la carrera\n"
    try:
        nota = float(nota)
        duracion = int(duracion)
    except (TypeError, ValueError):
        return jsonify({"error": "Valores inválidos para nota o duración"}), 400

    carrera_agregar = c.carrera(nombre, "", nota, duracion)
    dao.añadir_carrera(cursor, carrera_agregar)
    conexion.commit()

    print(f"[DEBUG] Carrera añadida: {nombre} (nota {nota}, {duracion} años)")
    return jsonify({"mensaje": f"Carrera '{nombre}' agregada correctamente"}), 201

@app.route('/actualizar/carrera/<int:id_carrera>', methods=['PUT'])
def api_actualizar_carrera(id_carrera):
    data = request.get_json()
    nombre = data.get("nombre")
    nota = data.get("nota_corte")
    duracion = data.get("duracion")

    if not nombre:
        return jsonify({"error": "Falta el nombre de la carrera"}), 400
    if not nota:
        return jsonify({"error": "Falta la nota  de la carrera"}), 400
    if not duracion:
        return jsonify({"error": "Falta la duracion de la carrera"}), 400

    try:
        nota = float(nota)
        duracion = int(duracion)
    except (TypeError, ValueError):
        return jsonify({"error": "Valores invalidos para nota o duracion"}), 400

    filas = dao.modificar_carrera(cursor, id_carrera, nombre, nota, duracion)
    conexion.commit()

    if filas == 0:
        return jsonify({"error": "Carrera no encontrada"}), 404

    print(f"[DEBUG] Carrera actualizada: {nombre} (ID {id_carrera})")
    return jsonify({"mensaje": f"Carrera '{nombre}' actualizada correctamente"}), 200

@app.route('/borrar/carrera/<int:id_carrera>', methods=['DELETE'])
def api_borrar_carrera(id_carrera):
    carrera_borrar = c.carrera(id_carrera=id_carrera)
    resultados = dao.borrar_carrera(cursor, carrera_borrar)
    conexion.commit()

    if not resultados:
        return jsonify({"error": "Carrera no encontrada"}), 404

    nombre = resultados[0]['Nombre_Carrera']
    print(f"[DEBUG] Carrera borrada: {nombre} (ID {id_carrera})")
    return jsonify({"mensaje": f"Carrera '{nombre}' eliminada correctamente"}), 200

if __name__ == "__main__":
    print("Servidor Flask en http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000, use_reloader=False)

