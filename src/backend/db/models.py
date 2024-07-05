import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Persona(db.Model):
    __tablename__ = "personas"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    contrasenia = db.Column(db.String(80), nullable=False)
    fecha_nacimiento = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    sexo = db.Column(db.String(20), nullable=False)
    domicilio = db.Column(db.String(80), nullable=False)


class Vehiculo(db.Model):
    __tablename__ = "vehiculos"
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(80), unique=True)  # UNIQUE
    fabricante = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)  # VALOR FLOAT
    persona_id = db.Column(
        db.Integer, db.ForeignKey("personas.id")
    )  # FORÁNEA A PERSONA


class Tramite(db.Model):
    __tablename__ = "tramites"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(256), nullable=False)
    valor = db.Column(db.Float, nullable=False)  # VALOR PRECIO FLOAT
    fecha_tramite = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    fecha_cita = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    persona_id = db.Column(
        db.Integer, db.ForeignKey("personas.id")
    )  # FORÁNEA A PERSONA


def get_all_personas() -> list[dict[str, str]] | None:
    try:
        personas = Persona.query.all()
        if not personas:
            return None
        personas_lista = []

        for persona in personas:
            personas_dict = {
                "id": persona.id,
                "nombre": persona.nombre,
                "apellido": persona.apellido,
                "email": persona.email,
                "contrasenia": persona.contrasenia,
                "fecha_nacimiento": persona.fecha_nacimiento.strftime("%Y-%m-%d"),
                "sexo": persona.sexo,
                "domicilio": persona.domicilio,
            }
            personas_lista.append(personas_dict)
        return personas_lista
    except Exception as e:
        print("Error en la base de datos, uy ", e)
        return None


# PRE: ID (entero) de la persona a buscar
# POST: Diccionario tabla/valor o NONE
def get_persona_por_id(id: int) -> dict[str, str] | None:
    # Consulta a la base de datos
    try:
        persona = Persona.query.get(id)
        if persona:
            return {
                "id": persona.id,
                "nombre": persona.nombre,
                "apellido": persona.apellido,
                "email": persona.email,
                "contrasenia": persona.contrasenia,
                "fecha_nacimiento": persona.fecha_nacimiento.strftime("%d-%m-%Y"),
                "sexo": persona.sexo,
                "domicilio": persona.domicilio,
            }
        return None
    except Exception as e:
        print(f"Error al consultar con la base de datos! {e}")
        return None


# PRE: Recibe una query Vehiculo.query.etc().all()
# POST: Devuelve una lista de diccionarios
def vehiculo_dict(vehiculos) -> list[dict[str, str]]:
    vehiculo_list = []
    for vehiculo in vehiculos:
        vehiculo_dict = {
            "id": vehiculo.id,
            "patente": vehiculo.patente,
            "fabricante": vehiculo.fabricante,
            "tipo": vehiculo.tipo,
            "modelo": vehiculo.modelo,
            "anio": vehiculo.anio,
            "valor": vehiculo.valor,
        }
        vehiculo_list.append(vehiculo_dict)
    return vehiculo_list


# PRE: Recibe una query Tramite.query.etc().all()
# POST: Devuelve una lista de diccionarios
def tramite_dict(tramites) -> list[dict[str, str]]:
    tramite_list = []
    for tramite in tramites:
        tramite_dict = {
            "id": tramite.id,
            "tipo": tramite.tipo,
            "valor": tramite.valor,
            "fecha_tramite": tramite.fecha_tramite,
            "fecha_cita": tramite.fecha_cita,
        }
        tramite_list.append(tramite_dict)
    return tramite_list


# PRE: id entero
# POST: Diccionario de una persona con vehiculos y tramites
def get_persona_full_info(id: int) -> dict[str, str] | None:
    try:
        persona = Persona.query.get(id)
        if not persona:
            return None
        tramites = Tramite.query.filter_by(persona_id=id).all()
        vehiculos = Vehiculo.query.filter_by(persona_id=id).all()
        persona_list = {
            "id": persona.id,
            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "email": persona.email,
            "contrasenia": persona.contrasenia,
            "fecha_nacimiento": persona.fecha_nacimiento.strftime("%Y-%m-%d"),
            "sexo": persona.sexo,
            "domicilio": persona.domicilio,
            "vehiculos": vehiculo_dict(vehiculos),
            "tramites": tramite_dict(tramites),
        }
        return persona_list
    except Exception as e:
        print("Uy quieto. Error :", e)
        return None


def editar_persona(persona: dict[str, str]) -> bool:
    return


def nueva_persona(persona: dict[str, str]) -> bool:
    return

#PRE: id entero
#POST: Booleano para indicando el estado de la eliminacion

def eliminar_persona(id: int) -> bool:
    encontrado = False
    try:
        persona = Persona.query.get(id)
        if persona:
            encontrado = True
            print('Persona ',persona.nombre," Eliminada correctamente.")
            db.session.delete(persona)
            db.session.commit()
        else:
            print("No se encontro un registro de la persona con id: ",id)
    except Exception as e:
        print("Uy, quieto. Error: ", e)
    return encontrado

def eliminar_tramite(id: int) -> bool:
    encontrado = False
    try:
        tramite = Tramite.query.get(id)
        if tramite:
            encontrado = True
            print('tramite ',tramite.nombre," Eliminada correctamente.")
            db.session.delete(tramite)
            db.session.commit()
        else:
            print("No se encontro un registro de la tramite con id: ",id)
    except Exception as e:
        print("Uy, quieto. Error: ", e)
    return encontrado

def eliminar_vehiculo(id: int) -> bool:
    encontrado = False
    try:
        vehiculo = Vehiculo.query.get(id)
        if vehiculo:
            encontrado = True
            print('vehiculo ',vehiculo.nombre," Eliminada correctamente.")
            db.session.delete(vehiculo)
            db.session.commit()
        else:
            print("No se encontro un registro de la vehiculo con id: ",id)
    except Exception as e:
        print("Uy, quieto. Error: ", e)
    return encontrado
