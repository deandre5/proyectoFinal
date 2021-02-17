from flask import Flask, jsonify, request
from flask_cors import CORS

from app.controllers.consultaEjercicios import consulta
from app.validators.agregarEjerciciosV import CreateExerciseSchema, UpdateExerciseSchema
from app.controllers.agregarEjercicios import agregar
from app.controllers.actualizarEjercicios import ActualizarEjercicios

exerciseSchema = CreateExerciseSchema()
updateExerciseSchema = UpdateExerciseSchema()


agregar_ejercicios = agregar()
consulta_Ejercicios = consulta()
actualizar_ejercicios = ActualizarEjercicios()

app = Flask(__name__)
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


@app.route('/agregarEjercicios', methods=['POST'])
def agregarEjercicios():
    try:
        content = request.get_json()

        validar = exerciseSchema.load(content)

        

        retorno = agregar_ejercicios.agregarEjercicios(content)

        

        if retorno:
           return jsonify({'status': 'ok'}), 200
        else:
            print("********************************")
            status = agregar_ejercicios.consultar(content)
            if status:
                return jsonify({'status': "bad", "message": "ya se encuentra registrada"}), 400
            else:
                return jsonify({'status': 'error', "message":"Error"}), 400


    
    except Exception as error:
        tojson = str(error)
        return jsonify({"status": "no es posible validar", "error": tojson}), 406





@app.route('/actualizarEjercicio/<int:id>', methods=['PUT'])
def actualizarEjercicio(id):
    try:
        id = str(id)

        content = request.get_json()

        validar = updateExerciseSchema.load(content)

        retorno = actualizar_ejercicios.actualizar(content, id)

        print(retorno,"-----------------")

        if isinstance(retorno, str):
            return jsonify({"status": "bad", "message": "Nombre ya se encuentra registrado"}), 406

        if retorno:
            return jsonify({"status":"ok"}), 200
        else:
            return jsonify({"status": "bad"}), 400
    except Exception as error:
        tojson = str(error)
        return jsonify({"status": "bad", "message": tojson }), 406