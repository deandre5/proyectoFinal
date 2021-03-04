import os
import bcrypt
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime, date, time
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import cloudinary.api

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


@app.route('/')
def index():
    return jsonify({'status': 'ok'})

# metodo que tiene un id como parametro, permitiendo la consulta de un ejercicio en especifico mediante ese id


@app.route('/consultaEjercicios/<int:id>', methods=['GET'])
def consultaEjerciociosId(id):

    # se encarga de enviar el id al controller: ConsultaEjercicios

    id = str(id)

    retorno = consulta_Ejercicios.consultaID(id)

    # examina si el retorno se hizo correctamente y devuelve los datos de este en json

    if retorno:
        return jsonify({'status': 'ok', 'ejercicio': retorno}), 200
    else:
        return jsonify({'status': 'error', "message": "No existe el ejercicio"}), 400

# metodo encargado de realizar una consulta general de los ejercicios


@app.route('/consultaEjercicios', methods=['GET'])
def consultaEjercicios():

    # funcion encargada de llamar al encagado de realizar el control
    retorno = consulta_Ejercicios.consultar()

    # examina si el retorno se hizo correctamente y devuelve los datos de este en json
    if retorno:
        return jsonify({'status': 'ok', 'ejercicios': retorno}), 200
    else:
        return jsonify({'status': 'error'}), 400


# metodo que recibe mediante post un json, luego valida y envia a la bd para registrar un ejercicio
@app.route('/agregarEjercicios', methods=['POST'])
def agregarEjercicios():
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
        dia = datetime.now()
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes(str(dia), encoding='utf-8'), salt)
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


# funcion que recibe como parametro un id, tambien recibe un json con la informacion para actualizar dicho ejercicio
@app.route('/actualizarEjercicio/<int:id>', methods=['PUT'])
def actualizarEjercicio(id):
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
            dia = datetime.now()
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes(str(dia), encoding='utf-8'), salt)
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


# funcion que recibe el parametro id del ejercicio
@app.route('/eliminarEjercicios/<int:id>', methods=['DELETE'])
def eliminarEjercicios(id):
    id = str(id)

    # envia el id al controller para su verificacion y posterior eliminacion
    retorno = eliminar_ejercicio.eliminar(id)

    if retorno:
        return jsonify({"status": "ok"}), 200

    else:
        return jsonify({"status": "bad", "message": "No existe el ejercicio"}), 400

# funcion que se encarga de recibir el json para el registro de las rutinas


@app.route('/registrarRutinas', methods=['POST'])
def registrarRutinas():
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


# funcion que recibe el id del usuario y un id de rutina para realizar su asignacion
@app.route('/asignarRutina/<int:id>/<int:idRutina>', methods=['POST'])
def asignarRutina(id, idRutina):
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


# funcion que recibe el id de la rutina para su posterior eliminacion
@app.route('/eliminarRutina/<int:id>', methods=['DELETE'])
def eliminarRutina(id):
    id = str(id)
    # se envia el id al controller para validar y luego eliminar
    retorno = eliminar.eliminarRutina(id)

    if retorno:
        return jsonify({"status": "ok"}), 200
    else:
        return jsonify({"status": "bad", "message": "no existe la rutina a eliminar"}), 400

# funcion que realiza una consulta a la rutina y la asociacion con los ejercicios


@app.route('/consultarRutinas', methods=['GET'])
def consultarRutinas():

    retorno = consultar_rutinas.consultar()

    if retorno:
        return jsonify({'status': 'ok', 'ejercicios': retorno}), 200
    else:
        return jsonify({'status': 'error'}), 400


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/uploader', methods=['POST'])
def uploader():
    try:
        if request.method == 'POST':

            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            tipo = request.form['tipo']
            print(nombre, descripcion, tipo)

            f = request.files['imagen']

            m = f.filename.split('.')

            if m[1] == "jpeg" or m[1] == "png" or m[1] == "jpg":

                print(m)

                dia = datetime.now()
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(bytes(str(dia), encoding='utf-8'), salt)
                h = str(hash).split('/')
                if len(h) > 2:
                    t = h[1]+h[2]
                else:
                    t = h[0]
                print(h, "----------------")
                filename = str(t)+"."+m[1]

                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                return "Archivo subido exitosamente"
            else:
                print(
                    "Por favor asegurese de que el nombre del archivo no incluya puntos")
                return "Por favor asegurese de que el nombre del archivo no incluya puntos"
    except Exception as error:
        print(error)
        return jsonify({"status": "error"}), 500
