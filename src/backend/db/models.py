from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""Funciones sql
ObjetoModelo.query.all() select all from ObjetoModelo
ObjetoModelo.query.get(id)
ObjetoModelo.query.filter_by( ObejoModelo.foreignKey = primaryKey).all()

ejemplo: Tramite.query.filter_by(persona_id=id).all()


db.session.add(ObjetoModelo) --> insert into tabla (ObjetoModelo)
db.session.commit() --> confirmar los cambios
db.session.rollback() --> cancelar los cambios
"""


class Persona(db.Model):
    __tablename__ = "personas"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    contrasenia = db.Column(db.String(80), nullable=False)
    fecha_nacimiento = db.Column(
        db.DateTime, nullable=False, default=datetime.now()
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
        db.DateTime, nullable=False, default=datetime.now()
    )
    fecha_cita = db.Column(db.DateTime, nullable=False, default=datetime.now())
    persona_id = db.Column(
        db.Integer, db.ForeignKey("personas.id")
    )  # FORÁNEA A PERSONA


def get_all_personas() -> list[dict[str, str]] | None:
    try:
        personas = Persona.query.order_by(Persona.id).all()
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
        db.session.rollback()
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
                # strftime convierte un datetime a texto
                "fecha_nacimiento": persona.fecha_nacimiento.strftime("%Y-%m-%d"),
                "sexo": persona.sexo,
                "domicilio": persona.domicilio,
            }
        return None
    except Exception as e:
        print("Error al consultar con la base de datos! ", e)
        db.session.rollback()
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
            "persona_id": vehiculo.persona_id,
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
            # strftime convierte un datetime a texto
            "fecha_nacimiento": persona.fecha_nacimiento.strftime("%d-%m-%Y"),
            "sexo": persona.sexo,
            "domicilio": persona.domicilio,
            "vehiculos": vehiculo_dict(vehiculos),
            "tramites": tramite_dict(tramites),
        }
        return persona_list
    except Exception as e:
        print("Uy quieto. Error :", e)
        db.session.rollback()
        return None


# PRE: id entero, dict de nueva_persona
# POST: Actualiza la persona en id, con los datos


def editar_persona(id: int, persona_editada: dict[str, str]) -> bool:
    editada = False
    try:
        persona = Persona.query.get(id)
        if persona:
            persona.nombre = persona_editada["nombre"]
            persona.apellido = persona_editada["apellido"]
            persona.email = persona_editada["email"]
            persona.contrasenia = persona_editada["contrasenia"]
            # strptime convierte un texto a objeto datetime
            persona.fecha_nacimiento = datetime.strptime(
                persona_editada["fecha_nacimiento"], "%Y-%m-%d"
            )
            persona.sexo = persona_editada["sexo"]
            persona.domicilio = persona_editada["domicilio"]

            db.session.commit()
            editada = True
        else:
            print("No se encontró un registro con la persona: ", id)
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        db.session.rollback()
    return editada


def nueva_persona(persona_nueva: dict[str, str]) -> bool:
    exito = False
    try:
        if Persona.query.filter_by(email=persona_nueva["email"]).first():
            print("El email esta en uso")
            return exito
        persona = Persona(
            nombre=persona_nueva["nombre"],
            apellido=persona_nueva["apellido"],
            email=persona_nueva["email"],
            contrasenia=persona_nueva["contrasenia"],
            fecha_nacimiento=datetime.strptime(
                persona_nueva["fecha_nacimiento"], "%Y-%m-%d"
            ),
            sexo=persona_nueva["sexo"],
            domicilio=persona_nueva["domicilio"],
        )
        db.session.add(persona)
        db.session.commit()
        exito = True
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        db.session.rollback()
    return exito


# PRE: id entero
# POST: Booleano para indicando el estado de la eliminacion


def eliminar_persona(id: int) -> bool:
    encontrado = False
    try:
        persona = Persona.query.get(id)
        if persona:
            encontrado = True
            print("Persona ", persona.nombre, " Eliminada correctamente.")
            #Eliminando foreign_keys
            Tramite.query.filter_by(persona_id=id).delete()
            Vehiculo.query.filter_by(persona_id=id).delete()
            
            db.session.delete(persona)
            db.session.commit()
        else:
            print("No se encontro un registro de la persona con id: ", id)
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        db.session.rollback()
    return encontrado


def nuevo_tramite(tramite_nuevo: dict[str, str]) -> bool:
    exito = False
    try:
        tramite = Tramite(
            tipo=tramite_nuevo["tipo"],
            valor=float(tramite_nuevo["valor"]),
            fecha_tramite=datetime.strptime(tramite_nuevo["fecha_tramite"], "%d-%m-%Y"),
            fecha_cita=datetime.strptime(tramite_nuevo["fecha_cita"], "%d-%m-%Y"),
            persona_id=int(tramite_nuevo["persona_id"]),
        )
        db.session.add(tramite)
        db.session.commit()
        exito = True
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        db.session.rollback()
    return exito


def eliminar_tramite(id: int) -> bool:
    encontrado = False
    try:
        tramite = Tramite.query.get(id)
        if tramite:
            encontrado = True
            print("tramite ", tramite.id, " Eliminada correctamente.")
            db.session.delete(tramite)
            db.session.commit()
        else:
            print("No se encontro un registro de la tramite con id: ", id)
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        db.session.rollback()
    return encontrado


def editar_tramite(id: int, tramite_editado: dict[str, str]) -> bool:
    editado = False
    try:
        tramite = Tramite.query.get(id)
        if tramite:
            tramite.tipo = tramite_editado["tipo"]
            tramite.fecha_tramite = datetime.strptime(tramite_editado["fecha_tramite"], "%d-%m-%Y")
            tramite.fecha_cita = datetime.strptime(tramite_editado["fecha_cita"], "%d-%m-%Y" )
            tramite.valor = float(tramite_editado["valor"])
            db.session.commit()
            editado = True
        else:
            print("Tramite ", id, " No encontrado :c")
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        db.session.rollback()
    return editado


def nuevo_vehiculo(vehiculo_nuevo: dict[str, str]) -> bool:
    exito = False
    try:
        if Vehiculo.query.filter_by(patente=vehiculo_nuevo["patente"]).first():
            print("La patente ya esta en uso")
            return exito
        vehiculo = Vehiculo(
            patente = vehiculo_nuevo["patente"],
            fabricante = vehiculo_nuevo["fabricante"],
            tipo = vehiculo_nuevo["tipo"],
            modelo = vehiculo_nuevo["modelo"],
            anio = int(vehiculo_nuevo["anio"]),
            valor = float(vehiculo_nuevo["valor"]),
            persona_id = int(vehiculo_nuevo["persona_id"]),           
        )
        db.session.add(vehiculo)
        db.session.commit()
        exito = True
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        db.session.rollback()    
    return exito

def editar_vehiculo(id: int, vehiculo_editado: dict[str, str]) -> bool:
    editado = False
    try:
        vehiculo = Vehiculo.query.get(id)
        if vehiculo:
            vehiculo.patente = vehiculo_editado["patente"]
            vehiculo.fabricante = vehiculo_editado["fabricante"]
            vehiculo.tipo = vehiculo_editado["tipo"]
            vehiculo.modelo = vehiculo_editado["modelo"]
            vehiculo.anio = int(vehiculo_editado["anio"])
            vehiculo.valor = float(vehiculo_editado["valor"])
            vehiculo.persona_id = int(vehiculo_editado["persona_id"])
            db.session.commit()
            editado = True
        else:
            print("Tramite ", id, " No encontrado :c")
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        db.session.rollback()
    return editado

def eliminar_vehiculo(id: int) -> bool:
    encontrado = False
    try:
        vehiculo = Vehiculo.query.get(id)
        if vehiculo:
            encontrado = True
            print("vehiculo ", vehiculo.id, " Eliminada correctamente.")
            db.session.delete(vehiculo)
            db.session.commit()
        else:
            print("No se encontro un registro de la vehiculo con id: ", id)
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        db.session.rollback()
    return encontrado

def get_vehiculos_por_persona(id: int) -> list[dict[str, str]] | None:
    try:
        vehiculos = Vehiculo.query.filter_by(persona_id=id).all()
        if not vehiculos:
            return None
        else:
            return vehiculo_dict(vehiculos)
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        return None


def get_tramites_por_persona(id: int) -> list[dict[str, str]] | None:
    try:
        tramites = Tramite.query.filter_by(persona_id=id).all()
        if not tramites:
            return None
        else:
            return tramite_dict(tramites)
    except Exception as e:
        print("Uy, quieto. Error: ", e)
        return None
