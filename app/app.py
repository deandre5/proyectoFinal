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

app = Flask(__name__)

cloudinary.config  (
  cloud_name = 'hdjsownnk',
  api_key = '926599253344788',
  api_secret = 'I8rBOy-rnozmrxhNL_Lg7hqtj7s'
)

app.config['UPLOAD_FOLDER'] = "../static"
CORS(app)

app.secret_key = 'esto-es-una-clave-muy-secreta'


@app.route('/')
def index():
    return jsonify({'status': 'ok'})

# metodo que tiene un id como parametro


@app.route('/consultaEjercicios/<int:id>', methods=['GET'])
def consultaEjerciociosId(id):

    # se encarga de enviar el id al controller: ConsultaEjercicios

    id = str(id)

    retorno = consulta_Ejercicios.consultaID(id)

    if retorno:
        return jsonify({'status': 'ok', 'ejercicio': retorno}), 200
    else:
        return jsonify({'status': 'error', "message": "No existe el ejercicio"}), 400


@app.route('/consultaEjercicios', methods=['GET'])
def consultaEjercicios():

    retorno = consulta_Ejercicios.consultar()

    if retorno:
        return jsonify({'status': 'ok', 'ejercicios': retorno}), 200
    else:
        return jsonify({'status': 'error'}), 400


# metodo que recibe mediante post un json, luego valida y envia a la bd para registrar un ejercicio
@app.route('/agregarEjercicios', methods=['POST'])
def agregarEjercicios():
    try:       

        #validar = exerciseSchema.load(content)
        
        validar = exerciseSchema.validate(request.form)


        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']
        

        f = request.files['imagen']

        filename = secure_filename(f.filename)

        dia = datetime.now()
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes(str(dia), encoding='utf-8'), salt)
        h = str(hash).split('/')
        if len(h) > 2:
                t = h[1]+h[2]
        else:
            t = h[0]
                
        filename = str(t)

        cloudinary.uploader.upload(f, public_id= filename)
        url = cloudinary.utils.cloudinary_url(filename)

        retorno = agregar_ejercicios.agregarEjercicios(nombre, descripcion, tipo, url[0])

        if retorno:
            
            return jsonify({'status': 'ok'}), 200
        else:
            print("********************************")
            status = agregar_ejercicios.consultar(nombre)
            if status:
                return jsonify({'status': "bad", "message": "ya se encuentra registrada"}), 400
            else:
                return jsonify({'status': 'error', "message": "Error"}), 400

    except Exception as error:
        tojson = str(error)
        print(tojson)
        return jsonify({"status": "no es posible validar", "error": tojson}), 406


@app.route('/actualizarEjercicio/<int:id>', methods=['PUT'])
def actualizarEjercicio(id):
    try:
        id = str(id)

        validar = exerciseSchema.validate(request.form)

        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        tipo = request.form['tipo']

        if len(request.files) > 0:

            f = request.files['imagen']
            filename = secure_filename(f.filename)


        

            dia = datetime.now()
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes(str(dia), encoding='utf-8'), salt)
            h = str(hash).split('/')
            if len(h) > 2:
                    t = h[1]+h[2]
            else:
                t = h[0]
                    
            filename = str(t)

            cloudinary.uploader.upload(f, public_id= filename)
            url = cloudinary.utils.cloudinary_url(filename)
            retorno = actualizar_ejercicios.actualizar(nombre, descripcion, tipo, id, url[0])

        else:
            f= request.form['url']
            retorno = actualizar_ejercicios.actualizar(nombre, descripcion, tipo, id, f)


            

        

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


@app.route('/eliminarEjercicios/<int:id>', methods=['DELETE'])
def eliminarEjercicios(id):
    id = str(id)

    retorno = eliminar_ejercicio.eliminar(id)

    if retorno:
        return jsonify({"status": "ok"}), 200

    else:
        return jsonify({"status": "bad", "message": "No existe el ejercicio"}), 400


@app.route('/registrarRutinas', methods=['POST'])
def registrarRutinas():
    try:
        content = request.get_json()

        validar = rutinasSchema.load(content)

        retorno = agregar_rutinas.agregar(content)

        if isinstance(retorno, str):
            return jsonify({"status": "bad", "message": "No existe el ejercicio a registrar"}), 406

        if retorno:
            return jsonify({'status': 'ok'}), 200

        else:

            status = agregar_rutinas.consulta(content)

            if status:
                return jsonify({'status': "bad", "message": "ya se encuentra registrada"}), 400
            else:
                return jsonify({'status': 'error', "message": "Error"}), 400

    except Exception as error:
        tojson = str(error)
        return jsonify({"status": "no es posible validar", "error": tojson}), 406


@app.route('/asignarRutina/<int:id>/<int:idRutina>', methods=['POST'])
def asignarRutina(id, idRutina):
    id = str(id)
    id_rutina = str(idRutina)

    retorno = Asignar.asignar(id, id_rutina)

    if isinstance(retorno, str):
        return jsonify({"status": "bad", "message": "No existe la rutina"}), 406

    if retorno:
        return jsonify({"status": "ok"}), 200

    else:
        return jsonify({"status": "bad", "message": "no existe el usuario"}), 400



@app.route('/eliminarRutina/<int:id>', methods=['DELETE'])
def eliminarRutina(id):
    id = str(id)
    retorno = eliminar.eliminarRutina(id)

    if retorno:
        return jsonify({"status": "ok"}),200
    else:
        return jsonify({"status": "bad", "message": "no existe la rutina a eliminar"}), 400


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
            print(nombre,descripcion,tipo)
            
            f = request.files['imagen']

            m = f.filename.split('.')

            if m[1]=="jpeg" or m[1]=="png" or m[1]=="jpg":

                print (m)

                dia = datetime.now()
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(bytes(str(dia), encoding='utf-8'), salt)
                h = str(hash).split('/')
                if len(h) > 2:
                    t = h[1]+h[2]
                else:
                    t = h[0]
                print(h,"----------------")
                filename = str(t)+"."+m[1]
                
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                return "Archivo subido exitosamente"
            else:
                print ("Por favor asegurese de que el nombre del archivo no incluya puntos")
                return "Por favor asegurese de que el nombre del archivo no incluya puntos"
    except Exception as error:
        print(error)
        return jsonify({"status": "error"}), 500