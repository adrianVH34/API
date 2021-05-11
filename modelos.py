from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    nombre = Column (String)
    apellido = Column (String)
    email = Column (String, unique = True)
    password = Column (String)

class Dato(db.Model):
    __tablename__ = 'datos'
    dato_id = Column(Integer, primary_key = True)
    dato = Column (Float)

class EsquemaUsuario(ma.Schema):
    class Meta:
        fields = ('id','nombre','apellido','email','password')

class EsquemaDato(ma.Schema):
    class Meta:
        fields = ('id','dato')

esUsuario = EsquemaUsuario()
esUsuarios = EsquemaUsuario(many=True)

esDato = EsquemaDato()
esDatos = EsquemaDato(many=True)