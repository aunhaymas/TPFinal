import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Persona(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique = True)
    contrasenia = db.Column(db.String(80), nullable=False)
    fecha_nacimiento = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    sexo = db.Column(db.String(20), nullable=False)
    domicilio = db.Column(db.String(80), nullable=False)


class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(80), unique=True)  # UNIQUE
    fabricante = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)  # VALOR FLOAT
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'))  # FORÁNEA A PERSONA

class Tramite(db.Model):
    __tablename__ = 'tramites'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(256), nullable=False)
    valor = db.Column(db.Float, nullable=False)  # VALOR PRECIO FLOAT
    fecha_tramite = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    fecha_cita = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'))  # FORÁNEA A PERSONA


# PRE: ID (entero) de la persona a buscar
# POST: Diccionario tabla/valor o NONE
def get_persona_por_id(id: int) -> dict[str, str] | None:
    # Consulta a la base de datos
    persona = Persona.query.get(id)

    try:
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
        
def nueva_persona() -> dict[str, str] | None:
    return 

def remove_persona(id: int) -> bool:
    encontrado = False
    return encontrado
