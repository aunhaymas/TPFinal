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
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 404


# CREAR PERSONA
@app.route("/personas", methods=["POST"])
def crear_persona():
    try:
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
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 404
    except Exception as e:
        print("Error al crear persona ", e)
        return jsonify({"message": "Error interno."}), 500


# EDITAR PERSONA


@app.route("/personas", methods=["PUT"])
def edit_persona():
    id = request.json.get("id_persona")
    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    email = request.json.get("email")
    contrasenia = request.json.get("contrasenia")
    fecha_nacimiento = request.json.get("fecha_nacimiento")
    sexo = request.json.get("sexo")
    domicilio = request.json.get("domicilio")
    persona_editada = {
        "id": id,
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "contrasenia": contrasenia,
        "fecha_nacimiento": fecha_nacimiento,
        "sexo": sexo,
        "domicilio": domicilio,
    }
    return jsonify({"success": editar_persona(id, persona_editada)})


# LISTAR TODOS LOS VEHICULOS DE TODAS LAS PERSONAS


@app.route("/vehiculos", methods=["GET"])
def listar_vehiculos():
    try:
        vehiculos = Vehiculo.query.order_by(Vehiculo.id).all()
        vehiculos_data = vehiculo_dict(vehiculos)
        return jsonify(vehiculos_data)
    except Exception as error:
        print("Error", error)
        return jsonify({'error': error})
    
    
# AÑADIR VEHICULO


@app.route("/vehiculos", methods=["POST"])
def crear_vehiculo():
    try:
        data = request.json

        patente = data.get("patente")
        fabricante = data.get("fabricante")
        tipo = data.get("tipo")
        modelo = data.get("modelo")
        anio = data.get("anio")
        valor = data.get("valor")
        persona_id = data.get("persona_id")
        vehiculo = {
            "patente": patente,
            "fabricante": fabricante,
            "tipo": tipo,
            "modelo": modelo,
            "anio": anio,
            "valor": valor,
            "persona_id": persona_id,
        }
        
        if(nuevo_vehiculo(vehiculo)):
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 404
    except Exception as error:
        print("Error!", error)
        return jsonify({"error": error}), 404
    

# ELIMINAR VEHICULO


@app.route("/vehiculos/<id>", methods=["DELETE"])
def remover_vehiculo(id):
    try:
        if(eliminar_vehiculo(id)):
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 404
    except Exception as error:
        print("Error al remover el vehiculo: ", error)
        return jsonify({"error": error}), 500


# DEVOLVER VEHICULO POR ID


@app.route("/vehiculos/<id>", methods=["GET"])
def obtener_vehiculo(id):
    try:
        vehiculo = Vehiculo.query.get(id)
        vehiculo_data = {
            'patente': vehiculo.patente,
            'fabricante': vehiculo.fabricante,
            'tipo': vehiculo.tipo,
            'modelo': vehiculo.modelo,
            'anio': vehiculo.anio,
            'valor': vehiculo.valor,
        }
        return jsonify(vehiculo_data), 200
    except Exception as e:
        return jsonify({"Error al obtener vehiculo: ",e}), 500
    

# EDITAR VEHICULO


@app.route("/vehiculos", methods=["PUT"])
def edit_vehiculo():
    try:
        id = request.json.get("id_vehiculo")
        patente = request.json.get("patente")
        fabricante = request.json.get("fabricante")
        tipo = request.json.get("tipo")
        modelo = request.json.get("modelo")
        anio = request.json.get("anio")
        valor = request.json.get("valor")
        persona_id = request.json.get("persona_id")
        vehiculo_editado = {
            "id": id,
            "patente": patente,
            "fabricante": fabricante,
            "tipo": tipo,
            "modelo": modelo,
            "anio": anio,
            "valor": valor,
            "persona_id": persona_id
        }
        return jsonify({"success": editar_vehiculo(id, vehiculo_editado)}), 200
    except Exception as error:
        print("Error!", error)
        return jsonify({"error": error}), 500



if __name__ == "__main__":
    print("Iniciando servidor...")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print("Servidor iniciado!")
    app.run(host="0.0.0.0", debug=True, port=port)
