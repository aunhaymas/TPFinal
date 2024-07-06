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
    personas = get_persona_con_vehiculos(1)
    print(personas)
    return """
<html>
<body>
<h1>Bienvenido al Penarer</h1>
<a href="/personas">Go to HomePage</a>
</body>
</html>
    """


# DEVOLVER JSON CON CHARS
@app.route("/personas")
def listar_personas():
    try:
        personas = Persona.query.all()
        personas_data = []
        for persona in personas:
            persona_data = {
                "nombre": persona.nombre,
                "apellido": persona.apellido,
                "email": persona.email,
                "contrasenia": persona.contrasenia,
                "dni": persona.dni,
                "fecha_nacimiento": persona.fecha_nacimiento,
                "sexo": persona.sexo,
                "domicilio": persona.domicilio,
            }
    except:
        return 1


# DEVOLVER PERSONA POR ID
@app.route("/personas/<id>")
def persona_id(id):
    return get_persona_por_id(id)


# ELIMINAR PERSONA
@app.route("/personas/<id>", methods=["DELETE"])
def remover_persona_por_id(id):
    return {"success": remover_persona_por_id(id)}


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
        "dni": dni,
        "fecha_nacimiento": fecha_nacimiento,
        "sexo": sexo,
        "domicilio": domicilio,
    }
    return {"success": add_character(character), "id": id}


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
