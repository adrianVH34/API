from flask import Flask, jsonify, request, render_template, redirect  # se importa flask 
from modelos import *
import numpy as np
import pickle
import os
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
''' Flask busca una applicacion apara correr 
esta linea le dice que solo busque este archivo como
la app'''

app =  Flask(__name__)
db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'baseDatos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secreta' # cambiarlo en la practica

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nuevaRuta')
def nuevaRuta():
    return jsonify(mensanje = "Esta es una nueva ruta", mensanje2 = "este es otro")

@app.route("/error")
def error():
    return jsonify(mensaje="Ese recurso no se encontro"), 404

@app.route("/parametros")
def parametros():
    nombre =  request.args.get('nombre')
    edad = int(request.args.get('edad'))
    if edad < 18:
        return jsonify(mensaje="Lo sentimos " + nombre + ", eres menor de edad"), 401 #401 no permitido
    else:
        return jsonify(mensaje="Bienvenido " + nombre + ", Puedes ingresar")

@app.route("/variable_url/<string:nombre>/<int:edad>")
def variable_url(nombre: str, edad: int):
    if edad < 18:
        return jsonify(mensaje="Lo sentimos " + nombre + ", eres menor de edad"), 401 #401 no permitido
    else:
        return jsonify(mensaje="Bienvenido " + nombre + ", Puedes ingresar") 

@app.route("/usuarios", methods = ['GET'])
def usuarios():
    listaUsuarios = User.query.all()
    resultado = esUsuarios.dump(listaUsuarios)
    return jsonify(resultado)


@app.route("/registro", methods=['Post'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()

    if test:
        return jsonify(mensaje='Ese email ya existe'), 409
    else:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        password = request.form['password']
        user = User(nombre = nombre,
                    apellido = apellido,
                    email = email,
                    password = password)
        db.session.add(user)
        db.session.commit() # importante!!!!
        return jsonify(mensaje = "Usuario creado correctamente"), 201

@app.route("/login", methods = ['Post'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email = email, password = password).first()
    if test:
        access_token = create_access_token(identity = email)
        return jsonify(mensaje =' Login exitoso', access_token = access_token)
    else:
        return jsonify(mensaje = 'email o password incorrectos'), 401

@app.route("/usuario/<int:idUsuario>", methods=["GET"])
def usuario(idUsuario:int):
    usuario = User.query.filter_by(id=idUsuario).first()
    if usuario:
        resultado = esUsuario.dump(usuario)
        return jsonify(resultado)
    else:
        return jsonify(mensaje = "Ese usurio no existe"),404

@app.route('/nuevoDato',  methods = ["POST"])
@jwt_required()
def nuevoDato():
    dato = request.form ['dato']    
    nuevoDato = Dato(dato = dato)
    db.session.add(nuevoDato)
    db.session.commit() # importante !!!!!!
    return  jsonify(mensaje = "nuevo dato agregado"),201


@app.route("/actulizarUsuario", methods=['PUT','POST'])
def actulizarUsuario():
    id =  int(request.form['id'])
    usuario = User.query.filter_by(id=id).first()
    if usuario:
        usuario.email = request.form['email']
        db.session.commit() #importante !!!!
        return jsonify(mensaje = "usted ha actulizado un usuario"), 202
    else:
        return jsonify(mensaje = "Ese usuario no existe")

@app.route("/eliminarDato/<int:dato_id>")
def eliminarDato(dato_id: int):
    dato = Dato.query.filter_by(dato_id = dato_id).first()
    if dato:
        db.session.delete(dato)
        db.session.commit() #importante!!!!!
        return jsonify(mensaje ='Dato eliminado'), 202
    else:
        return jsonify(mensaje = "Ese dato no existe")

@app.route('/loginGrafico', methods = ['Post'])
def loginGrafico():
    email = request.form['email']
    password = request.form['password']

    test = User.query.filter_by(email = email, password = password).first()
    if test:
        access_token = create_access_token(identity = email)
        return render_template('login.html',access_token = access_token)
    else:
        return redirect("/")

@app.route('/predecir', methods=['GET','POST'])
def predecir():
    if request.method == "POST":
        listaString = []
        listaFloat = []
        m = ""
        
        data = request.form.to_dict()
        datos = list(data.values())
        for dato in datos:
            listaFloat.append(float(dato))
        listaFloat = np.array(listaFloat)

        clf2 = pickle.load( open( "entrenado.p", "rb" ) )    
        predecir=clf2.predict(listaFloat.reshape(1,-1))
        if predecir == 1:
            m = "Posiblemente diabetico"
        else:
            m = "Posiblemente NO ES diabetico"         
        
    return m

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0')
