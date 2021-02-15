from flask import Flask, jsonify, request
from flask_cors import CORS

from app.controllers.consultaEjercicios import consulta


consulta_Ejercicios = consulta()

app = Flask(__name__)
CORS(app)

app.secret_key = 'esto-es-una-clave-muy-secreta'


@app.route('/')
def index():
    return jsonify({'status':'ok'})

#metodo que tiene un id como parametro
@app.route('/consulta/<id>', methods=['GET'])
def consultaEjerciociosId(id):
    

    #se encarga de enviar el id al controller: ConsultaEjercicios
    retorno = consulta_Ejercicios.consultaID(id)

    if retorno:
        return jsonify({'status':'ok', 'ejercicio': retorno}), 200
    else:
        return jsonify({'status':'error'}), 400

@app.route('/consulta', methods=['GET'])
def consultaEjercicios():

    
    retorno = consulta_Ejercicios.consultar()

    if retorno:
        return jsonify({'status':'ok', 'ejercicios': retorno}),200
    else:
        return jsonify({'status':'error'}), 400
