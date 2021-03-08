import os
import bcrypt
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import datetime
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import cloudinary.api
import bcrypt
import jwt

from app.config.config import KEY_TOKEN_AUTH

from app.controllers.consultaEjercicios import consulta

from app.controllers.agregarEjercicios import agregar
from app.controllers.actualizarEjercicios import ActualizarEjercicios
from app.controllers.eliminarEjercicio import Eliminar

from app.controllers.registrarRutinas import AgregarRutina
from app.controllers.asignarRutina import Asignar
from app.controllers.eliminarRutina import eliminar
from app.controllers.consultarRutinas import consultarRutinas

from app.validators.agregarEjerciciosV import CreateExerciseSchema
from app.validators.rutinasValidate import CreateRoutineSchema

exerciseSchema = CreateExerciseSchema()
rutinasSchema = CreateRoutineSchema()

eliminar_ejercicio = Eliminar()
agregar_ejercicios = agregar()
consulta_Ejercicios = consulta()
actualizar_ejercicios = ActualizarEjercicios()


agregar_rutinas = AgregarRutina()
asignar_rutina = Asignar()
eliminar_rutina = eliminar()
consultar_rutinas = consultarRutinas()

app = Flask(__name__)

# configuracion de la api cloudinary, se ingresan las credenciales dadas por la api
cloudinary.config(
    cloud_name='hdjsownnk',
    api_key='926599253344788',
    api_secret='I8rBOy-rnozmrxhNL_Lg7hqtj7s'
)


CORS(app)

app.secret_key = 'esto-es-una-clave-muy-secreta'

# funcion que crea un token, teniendo un admin como usuario


@app.route('/admin')
def index():
    encode_jwt = jwt.encode({'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(seconds=180), "user": "admin"}, KEY_TOKEN_AUTH, algorithm='HS256')

    print(encode_jwt)

    return jsonify({"status": "ok", "token": encode_jwt})


# funcion que crea un token, teniendo un user como usuario
@app.route('/user')
def user():
    encode_jwt = jwt.encode({'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(seconds=180), "user": "user"}, KEY_TOKEN_AUTH, algorithm='HS256')

    print(encode_jwt)

    return jsonify({"status": "ok", "token": encode_jwt})


# funcion que valida el token
def validacion(headers):
    token = headers.split(' ')

    try:
        # se devulve la informacion util del usuario
        data = jwt.decode(token[1], KEY_TOKEN_AUTH, algorithms=['HS256'])
        status = True
        print(data)
        return data
    except:
        status = False
        return status

# metodo que tiene un id como parametro, permitiendo la consulta de un ejercicio en especifico mediante ese id


@app.route('/consultaEjercicios/<int:id>', methods=['GET'])
def consultaEjerciociosId(id):

    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:

            # se encarga de enviar el id al controller: ConsultaEjercicios

            id = str(id)

            retorno = consulta_Ejercicios.consultaID(id)

            # examina si el retorno se hizo correctamente y devuelve los datos de este en json

            if retorno:
                return jsonify({'status': 'ok', 'ejercicio': retorno}), 200
            else:
                return jsonify({'status': 'error', "message": "No existe el ejercicio"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


# metodo encargado de realizar una consulta general de los ejercicios
@app.route('/consultaEjercicios', methods=['GET', 'POST'])
def consultaEjercicios():

    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:

            # funcion encargada de llamar al encagado de realizar el control
            retorno = consulta_Ejercicios.consultar()

            # examina si el retorno se hizo correctamente y devuelve los datos de este en json
            if retorno:
                return jsonify({'status': 'ok', 'ejercicios': retorno}), 200
            else:
                return jsonify({'status': 'error'}), 400

        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


# metodo que recibe mediante post un json, luego valida y envia a la bd para registrar un ejercicio
@app.route('/agregarEjercicios', methods=['POST'])
def agregarEjercicios():
    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                try:

                    # realiza las validaciones al form que recibe
                    validar = exerciseSchema.validate(request.form)

                    nombre = request.form['nombre']
                    descripcion = request.form['descripcion']
                    tipo = request.form['tipo']

                    # variable que obtiene como valor la imagen enviada desde el cliente
                    f = request.files['imagen']

                    # se encarga de revizar que el nombre del archivo no sea un problema para nuestro programa
                    filename = secure_filename(f.filename)

                    # se encripta el dia actual, la hora y se genera un salt, luego el salt se divide en partes mediante el /
                    dia = datetime.datetime.utcnow()
                    salt = bcrypt.gensalt()
                    hash = bcrypt.hashpw(
                        bytes(str(dia), encoding='utf-8'), salt)
                    h = str(hash).split('/')

                    # se reviza el len de h para poder determinar su nombe proviniente del hash
                    if len(h) > 2:
                        t = h[1]+h[2]
                    else:
                        t = h[0]

                    filename = str(t)

                    # se llama a la api y se registra la imagen y el nombre al cual le hicimos hash, luego obtenemos la url para enviarla al controller
                    cloudinary.uploader.upload(f, public_id=filename)
                    url = cloudinary.utils.cloudinary_url(filename)

                    # se envian los datos al controller para su registro
                    retorno = agregar_ejercicios.agregarEjercicios(
                        nombre, descripcion, tipo, url[0])

                    # se examina si se registro la informacion en la base de datos
                    if retorno:

                        return jsonify({'status': 'ok'}), 200
                    else:
                        # se examina si el nombre esta repetido en la base de datos
                        status = agregar_ejercicios.consultar(nombre)
                        if status:
                            return jsonify({'status': "bad", "message": "ya se encuentra registrada"}), 400
                        else:
                            return jsonify({'status': 'error', "message": "Error"}), 400

                except Exception as error:
                    tojson = str(error)
                    print(tojson)
                    return jsonify({"status": "no es posible validar", "error": tojson}), 406
            else:
                return jsonify({'status': 'error', "message": "No tiene permisos para entrar a esta pagina"}), 406
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


# funcion que recibe como parametro un id, tambien recibe un json con la informacion para actualizar dicho ejercicio
@app.route('/actualizarEjercicio/<int:id>', methods=['PUT'])
def actualizarEjercicio(id):
    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                try:
                    id = str(id)

                    # realiza las validaciones al form que recibe
                    validar = exerciseSchema.validate(request.form)

                    nombre = request.form['nombre']
                    descripcion = request.form['descripcion']
                    tipo = request.form['tipo']

                    # si el len de los archivos enviados es mayor que 0, guarda la imagen y envia la nueva url para su registro en la base de datos
                    if len(request.files) > 0:
                        # variable que obtiene como valor la imagen enviada desde el cliente
                        f = request.files['imagen']

                        # se encarga de revizar que el nombre del archivo no sea un problema para nuestro programa

                        filename = secure_filename(f.filename)

                        # se encripta el dia actual, la hora y se genera un salt, luego el salt se divide en partes mediante el /
                        dia = datetime.datetime.utcnow()
                        salt = bcrypt.gensalt()
                        hash = bcrypt.hashpw(
                            bytes(str(dia), encoding='utf-8'), salt)
                        h = str(hash).split('/')

                        # se reviza el len de h para poder determinar su nombe proviniente del hash
                        if len(h) > 2:
                            t = h[1]+h[2]
                        else:
                            t = h[0]

                        filename = str(t)
                        # se llama a la api y se registra la imagen y el nombre al cual le hicimos hash, luego obtenemos la url para enviarla al controller
                        cloudinary.uploader.upload(f, public_id=filename)
                        url = cloudinary.utils.cloudinary_url(filename)

                        # se envian los datos al controller para su registro
                        retorno = actualizar_ejercicios.actualizar(
                            nombre, descripcion, tipo, id, url[0])

                    else:
                        # si no se envian imagenes, se recupera al anterior url y se envia al controller para su registro
                        f = request.form['url']
                        retorno = actualizar_ejercicios.actualizar(
                            nombre, descripcion, tipo, id, f)

                    # si retorno es una instancia de string nos damos cuenta que el nombre esta registrado
                    if isinstance(retorno, str):

                        return jsonify({"status": "bad", "message": "Nombre ya se encuentra registrado"}), 406

                    if retorno:
                        return jsonify({"status": "ok"}), 200
                    else:
                        return jsonify({"status": "bad"}), 400
                except Exception as error:
                    tojson = str(error)
                    print(error)
                    return jsonify({"status": "bad", "message": tojson}), 406
            else:
                return jsonify({"status": "bad", "message": "No tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


# funcion que recibe el parametro id del ejercicio
@app.route('/eliminarEjercicios/<int:id>', methods=['DELETE'])
def eliminarEjercicios(id):

    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                id = str(id)

                # envia el id al controller para su verificacion y posterior eliminacion
                retorno = eliminar_ejercicio.eliminar(id)

                if retorno:
                    return jsonify({"status": "ok"}), 200

                else:
                    return jsonify({"status": "bad", "message": "No existe el ejercicio"}), 400
            else:
                return jsonify({'status': 'bad', "message": "No tiene permisos para acceder"})
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


# funcion que se encarga de recibir el json para el registro de las rutinas
@app.route('/registrarRutinas', methods=['POST'])
def registrarRutinas():
    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                try:
                    # se recibe el json y se validan los campos de este
                    content = request.get_json()

                    validar = rutinasSchema.load(content)

                    # se envia el json para su registro
                    retorno = agregar_rutinas.agregar(content)

                    # si se recibe un string esto indica que no existe el ejercicio a registrar

                    if isinstance(retorno, str):
                        return jsonify({"status": "bad", "message": "No existe el ejercicio a registrar"}), 406

                    if retorno:
                        return jsonify({'status': 'ok'}), 200

                    else:
                        # se valida si el nombre de la rutina ya existe en la base de datos
                        status = agregar_rutinas.consulta(content)

                        if status:
                            return jsonify({'status': "bad", "message": "ya se encuentra registrada"}), 400
                        else:
                            return jsonify({'status': 'error', "message": "Error"}), 400

                except Exception as error:
                    tojson = str(error)
                    return jsonify({"status": "no es posible validar", "error": tojson}), 406
            else:
                return jsonify({"status": "bad", "message": "No tiene permisos para acceder"})
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


# funcion que recibe el id del usuario y un id de rutina para realizar su asignacion
@app.route('/asignarRutina/<int:id>/<int:idRutina>', methods=['POST'])
def asignarRutina(id, idRutina):

    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                id = str(id)
                id_rutina = str(idRutina)

                retorno = Asignar.asignar(id, id_rutina)

                # si el sistema devuelve un string es por que la rutina no existe
                if isinstance(retorno, str):
                    return jsonify({"status": "bad", "message": "No existe la rutina"}), 406

                if retorno:
                    return jsonify({"status": "ok"}), 200

                else:
                    return jsonify({"status": "bad", "message": "no existe el usuario"}), 400
            else:
                return jsonify({"status": "bad", "message": "no tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


# funcion que recibe el id de la rutina para su posterior eliminacion
@app.route('/eliminarRutina/<int:id>', methods=['DELETE'])
def eliminarRutina(id):
    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                id = str(id)
                # se envia el id al controller para validar y luego eliminar
                retorno = eliminar.eliminarRutina(id)

                if retorno:
                    return jsonify({"status": "ok"}), 200
                else:
                    return jsonify({"status": "bad", "message": "no existe la rutina a eliminar"}), 400
            else:
                return jsonify({"status": "bad", "message": "no tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


# funcion que realiza una consulta a la rutina y la asociacion con los ejercicios
@app.route('/consultarRutinas', methods=['GET'])
def consultarRutinas():

    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:

            retorno = consultar_rutinas.consultar()

            if retorno:
                return jsonify({'status': 'ok', 'ejercicios': retorno}), 200
            else:
                return jsonify({'status': 'error'}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})
