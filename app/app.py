import os
import bcrypt
from flask import Flask, jsonify, request, render_template, Response
from flask_cors import CORS
import datetime
from werkzeug.utils import secure_filename
from app.helpers.helpers import KEY_TOKEN_AUTH, validacion, validacionToken
import bcrypt
import io
import xlwt


from app.controllers.consultaEjercicios import consulta

from app.controllers.agregarEjercicios import agregar
from app.controllers.actualizarEjercicios import ActualizarEjercicios
from app.controllers.eliminarEjercicio import Eliminar

from app.controllers.registrarRutinas import AgregarRutina
from app.controllers.asignarRutina import Asignar
from app.controllers.eliminarRutina import eliminar
from app.controllers.consultarRutinas import consultarRutinas
from app.controllers.actualizarRutina import ActualizarRutina
from app.controllers.ReporteRutina import ReporteRutina

from app.controllers.registroDietas import AgregarDietas
from app.controllers.consultarDietas import ConsultaDietas
from app.controllers.asignarDieta import AsignarDietas
from app.controllers.eliminarDieta import EliminarDietas
from app.controllers.actualizarDieta import ActualizarDieta
from app.controllers.reporteDietas import ReporteDietas

from app.validators.agregarEjerciciosV import CreateExerciseSchema
from app.validators.rutinasValidate import CreateRoutineSchema
from app.validators.dietasValidate import CreateDietSchema

exerciseSchema = CreateExerciseSchema()
rutinasSchema = CreateRoutineSchema()
dietaSchema = CreateDietSchema()

eliminar_ejercicio = Eliminar()
agregar_ejercicios = agregar()
consulta_Ejercicios = consulta()
actualizar_ejercicios = ActualizarEjercicios()


agregar_rutinas = AgregarRutina()
asignar_rutina = Asignar()
eliminar_rutina = eliminar()
consultar_rutinas = consultarRutinas()
actualizar_rutina = ActualizarRutina()
reporte_rutina = ReporteRutina()

registro_dietas = AgregarDietas()
consulta_dietas = ConsultaDietas()
asignar_dieta = AsignarDietas()
eliminar_dieta = EliminarDietas()
actualizar_dieta = ActualizarDieta()
reporte_dietas = ReporteDietas()

app = Flask(__name__)

# configuracion de la api cloudinary, se ingresan las credenciales dadas por la api


CORS(app)


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
            return jsonify({'status': 'error', "message": "Token invalido"}), 400
    else:
        return jsonify({'status': 'No ha envido ningun token'}), 400


# metodo que recibe mediante post un json, luego valida y envia a la bd para registrar un ejercicio


@app.route('/agregarEjercicios', methods=['POST'])
def agregarEjercicios():
    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                try:

                    if len(request.files):

                        # realiza las validaciones al form que recibe
                        validar = exerciseSchema.validate(request.form)

                        content = request.form

                        # variable que obtiene como valor la imagen enviada desde el cliente
                        file = request.files['imagen']

                        # se envian los datos al controller para su registro
                        retorno = agregar_ejercicios.agregarEjercicios(
                            content, file)

                        # se examina si se registro la informacion en la base de datos

                        if retorno == 0:
                            return jsonify({'status': 'Porfavor ingrese un archivo valido'}), 400
                        if retorno:

                            return jsonify({'status': 'ok'}), 200
                        else:
                            nombre = request["nombre"]
                            # se examina si el nombre esta repetido en la base de datos
                            status = agregar_ejercicios.consultar(nombre)
                            if status:
                                return jsonify({'status': "bad", "message": "ya se encuentra registrada"}), 400
                            else:
                                return jsonify({'status': 'error', "message": "Error"}), 400

                    else:
                        return jsonify({'status': 'Error, No ha subido ninguna imagen'}), 400

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

                    content = request.form

                    # si el len de los archivos enviados es mayor que 0, guarda la imagen y envia la nueva url para su registro en la base de datos
                    if len(request.files) > 0:
                        # variable que obtiene como valor la imagen enviada desde el cliente

                        file = request.files['imagen']

                        actualizar = actualizar_ejercicios.actualizarConfoto(
                            id, content, file)

                        if actualizar == 0:
                            return jsonify({"status": "Ingrese un archivo valido"}), 400

                        if isinstance(actualizar, str):
                            return jsonify({"status": "Ya se encuentra registrado el ejercicio"}), 400

                        if actualizar:
                            return jsonify({"status": "OK"}), 200

                        else:
                            return jsonify({"status": "Error, no existe el ejercicio"}), 400

                    else:

                        actualizar = actualizar_ejercicios.actualizarSinFoto(
                            id, content)

                        if isinstance(actualizar, str):
                            return jsonify({"status": "Ya se encuentra registrado el ejercicio"}), 400

                        if actualizar:
                            return jsonify({"status": "OK"}), 200

                        else:
                            return jsonify({"status": "Error, no existe el ejercicio"})

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
                return jsonify({'status': 'bad', "message": "No tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"}), 400
    else:
        return jsonify({'status': 'No ha envido ningun token'}), 400


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

                    validarRutina = rutinasSchema.load(content)

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

# funcion que recibe un id para actualizar una rutina


@app.route('/actualizarRutina/<int:id>', methods=['PUT'])
def actualizarRutina(id):

    if request.headers.get('Authorization'):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":

                id = str(id)

                content = request.get_json()

                validarRutina = rutinasSchema.load(content)

                retorno = actualizar_rutina.actualizarRutina(content, id)

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

            else:
                return jsonify({"status": "bad", "message": "no tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


# funcion que recibe el id del usuario y un id de rutina para realizar su asignacion
@app.route('/asignarRutina/<int:id>/<int:idRutina>', methods=['PUT'])
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


@app.route('/consultarRutinas/<int:id>', methods=['GET'])
def consultarRutinasID(id):

    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:

            id = str(id)

            retorno = consultar_rutinas.consultaID(id)

            if retorno:
                return jsonify({'status': 'ok', 'ejercicios': retorno}), 200
            else:
                return jsonify({'status': 'error'}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"}), 400
    else:
        return jsonify({'status': 'No ha envido ningun token'}), 400


@app.route('/reporteRutinas', methods=['GET'])
def reporteRutinas():

    if(request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":

                retorno = reporte_rutina.generarReporte()
                return Response(retorno, mimetype="application/ms-excel", headers={"content-Disposition": "attachment; filename=reporteRutinas.csv"})

            else:
                return jsonify({"status": "bad", "message": "no tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


@app.route('/registrarDietas', methods=['POST'])
def registrarDietas():

    if(request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacionToken(validar)

        if validate:
            if validate.get('user') == "admin":

                try:

                    content = request.get_json()

                    validacion = dietaSchema.load(content)

                    retorno = registro_dietas.agregarDieta(content)

                    if isinstance(retorno, str):
                        return jsonify({"status": "bad", "message": "ya existe una dieta con ese nombre"}), 406

                    if retorno:
                        return jsonify({"status": "Dieta registrada"}), 200

                    else:
                        return jsonify({"status": "bad", "error": "Error"}), 406

                except Exception as error:
                    tojson = str(error)
                    return jsonify({"status": "no es posible validar", "error": tojson}), 406
            else:
                return jsonify({"status": "bad", "message": "no tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"}), 406
    else:
        return jsonify({'status': 'No ha envido ningun token'}), 406


@app.route('/consultarDietas', methods=['GET'])
def consultarDietas():

    if(request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacionToken(validar)
        if validate:
            retorno = consulta_dietas.consulta()

            if retorno:
                return jsonify({'status': 'ok', "dietas": retorno}), 200

            else:
                return jsonify({'status': 'error'}), 400

        else:
            return jsonify({'status': 'error', "message": "Token invalido"}), 406
    else:
        return jsonify({'status': 'No ha envido ningun token'}), 406


@app.route('/consultarDietas/<int:id>', methods=['GET'])
def consultarDietasID(id):

    if(request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacionToken(validar)
        if validate:

            id = str(id)

            retorno = consulta_dietas.consultaID(id)

            if retorno:
                return jsonify({'status': 'ok', 'dietas': retorno}), 200
            else:
                return jsonify({'status': 'error'}), 400

        else:
            return jsonify({'status': 'error', "message": "Token invalido"}), 406
    else:
        return jsonify({'status': 'No ha envido ningun token'}), 406


@app.route('/asignarDieta/<int:idDieta>/<int:id>', methods=['PUT'])
def asignarDieta(idDieta, id):
    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                id = str(id)
                idDieta = str(idDieta)

                retorno = asignar_dieta.asignar(idDieta, id)

                # si el sistema devuelve un string es por que la rutina no existe
                if isinstance(retorno, str):
                    return jsonify({"status": "bad", "message": "No existe la dieta"}), 406

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


@app.route('/eliminarDietas/<int:id>', methods=['DELETE'])
def eliminarDietas(id):
    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                id = str(id)

                retorno = eliminar_dieta.eliminar(id)

                if retorno:
                    return jsonify({"status": "ok"}), 200
                else:
                    return jsonify({"status": "bad", "message": "no existe la dieta a eliminar"}), 400

            else:
                return jsonify({"status": "bad", "message": "no tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


@app.route('/actualizarDietas/<int:id>', methods=['PUT'])
def actualizarDietas(id):
    if (request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":
                id = str(id)

                content = request.get_json()

                try:

                    validarJson = dietaSchema.load(content)

                    retorno = actualizar_dieta.actualizar(id, content)

                    if isinstance(retorno, str):

                        return jsonify({"status": "bad", "message": "Nombre ya se encuentra registrado"}), 406

                    if retorno:
                        return jsonify({"status": "ok"}), 200
                    else:
                        return jsonify({"status": "bad"}), 400

                except Exception as error:
                    tojson = str(error)
                    return jsonify({"status": "no es posible validar", "error": tojson}), 406

            else:
                return jsonify({"status": "bad", "message": "no tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


@app.route('/reporteDietas', methods=['GET'])
def reporteDietas():

    if(request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:
            if validate.get('user') == "admin":

                retorno = reporte_dietas.generarReporte()
                return Response(retorno, mimetype="application/ms-excel", headers={"content-Disposition": "attachment; filename=reporteDietas.csv"})

            else:
                return jsonify({"status": "bad", "message": "no tiene permisos para acceder"}), 400
        else:
            return jsonify({'status': 'error', "message": "Token invalido"})
    else:
        return jsonify({'status': 'No ha envido ningun token'})


@app.route('/ejercicios')
def ejercicios():

    if(request.headers.get('Authorization')):
        validar = request.headers.get('Authorization')

        validate = validacion(validar)

        if validate:

            ejercicios = consulta_Ejercicios.ejercicios()

            if ejercicios:
                return jsonify({"status": "OK", "Ejercicios": ejercicios}), 200
            else:
                return jsonify({"status": "No hay ejercicios registrados"}), 400

        else:
            return jsonify({'status': 'error', "message": "Token invalido"}), 406
    else:
        return jsonify({'status': 'No ha envido ningun token'}), 406
