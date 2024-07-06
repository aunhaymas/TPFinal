from flask import Flask, request, jsonify
from flask_cors import CORS

from db.models import *

# for multi-server communication
app = Flask(__name__)
port = 5000
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:123@localhost:5432/renaper"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)


# HOME
@app.route("/")
def home():
    personas = get_persona_full_info(1)
    print(personas)
    return """
<html>
<body>
<h1>Bienvenido al Penarer</h1>
<a href="/personas">Go to HomePage</a>
</body>
</html>
    """


# DEVOLVER JSON CON PERSONAS
@app.route("/personas")
def listar_personas():
    try:
        personas =  get_all_personas()
        if personas != None:
            return jsonify(personas), 200
        else:
            return jsonify({"Error: ": "No hay personas en la base de datos"}), 404
    except Exception as e:
        return jsonify({"Error: ": e}), 500

# DEVOLVER TRAMITES POR PERSONA ID
@app.route("/personas/<id>/tramites")
def listar_tramites_por_persona(id):
    try:
        tramites = get_tramites_por_persona(id)
        if tramites:
            return jsonify(tramites), 200
        else:
            return jsonify({"Error: ": f"No hay tramites en la base de datos para esta persona {id}"}), 404
    except Exception as e:
        return jsonify({"Error: ", e}), 500
# DEVOLVER VEHICULOS POR PERSONA ID
@app.route("/personas/<id>/vehiculos",methods=["GET"])
def listar_vehiculos_por_persona(id):
    try:
        vehiculos = get_vehiculos_por_persona(id)
        if vehiculos:
            return jsonify(vehiculos), 200
        else:
            return jsonify({"Error: ": f"No hay vehiculos en la base de datos para esta persona {id}"}), 404
    except Exception as e:
        return jsonify({"Error: ", e}), 500            

# DEVOLVER PERSONA POR ID
@app.route("/personas/<id>",methods=["GET"])
def persona_id(id):
    try:
        persona = get_persona_por_id(id)
        if persona != None:
            return jsonify(persona),200
        else:
            return jsonify({"error": f"Persona no encontrada con id: {id}"}), 404
    except Exception as e:
        return jsonify({"Error al obtener persona: ",e}), 500



# ELIMINAR PERSONA
@app.route("/personas/<id>", methods=["DELETE"])
def remover_persona(id):
        if eliminar_persona(id):
            return jsonify({"message": "Persona eliminada correctamente."}), 200
        else:
            return jsonify({"message": "Persona no encontrada."}), 404


# CREAR PERSONA
@app.route("/personas", methods=["POST"])
def crear_persona():
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    contrasenia = data.get("contrasenia")
    fecha_nacimiento = data.get("fecha_nacimiento")
    sexo = data.get("sexo")
    domicilio = data.get("domicilio")
    persona = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "contrasenia": contrasenia,
        "fecha_nacimiento": fecha_nacimiento,
        "sexo": sexo,
        "domicilio": domicilio,
    }
    if nueva_persona(persona):
        return jsonify({"message": "Persona creada correctamente."}), 200
    else:
        return jsonify({"message": "No se pudo crear a la persona. Error en el formato de fecha?"}), 404


# EDITAR PERSONA


@app.route("/personas", methods=["PUT"])
def _edit_persona():
    id = request.json.get("id")
    name = request.json.get("name")
    names = request.json.get("names")
    alignment = request.json.get("alignment")
    gender = request.json.get("gender")
    publisher = request.json.get("publisher")
    race = request.json.get("race")
    image = request.json.get("image")
    character = {
        "id": id,
        "gender": gender,
        "alignment": alignment,
        "image": image,
        "name": name,
        "names": names,
        "publisher": publisher,
        "race": race,
    }
    return {"success": edit_character(character)}


if __name__ == "__main__":
    print("Iniciando servidor...")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print("Servidor iniciado!")
    app.run(host="0.0.0.0", debug=True, port=port)
