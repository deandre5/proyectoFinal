from app.model.ejerciciosModel import Ejercicios
from app.helpers.helpers import allowed_file
import cloudinary
import cloudinary.uploader
import cloudinary.api
import datetime
import bcrypt
from werkzeug.utils import secure_filename


cloudinary.config(
    cloud_name='hdjsownnk',
    api_key='926599253344788',
    api_secret='I8rBOy-rnozmrxhNL_Lg7hqtj7s'
)


ejercicios = Ejercicios()


class ActualizarEjercicios:

    # funcion que recibe los datos del ejercicio a actualizar
    def actualizarConfoto(self, id, content, file):

        try:

            nombre = content['nombre']

            # se verifica que el nombre no este repetido en la base de datos
            verificarNombre = ejercicios.consultarEjercicioActualizar(nombre)

            # si el nombre esta repetido se envian string de esta forma se conoce el motivo
            if verificarNombre:
                status = "mal"
                return status

            # se verifica que el id enviado exista en la base de datos
            verificarId = ejercicios.ConsultaId(id)

            # si el len de verificarId es menor que 1 quiere decir que no existe este ejercicio en la base de datos
            if len(verificarId) < 1:
                status = False
                return status

            if allowed_file(file.filename):

                descripcion = content['descripcion']
                tipo = content['tipo']

                filename = secure_filename(file.filename)

                dia = datetime.datetime.utcnow()
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(bytes(str(dia), encoding='utf-8'), salt)

                h = str(hash).split('/')

                if (len(h) > 2):
                    t = h[1]+h[2]
                else:
                    t = h[0]

                filename = h[0]

                filename = str(t)

                cloudinary.uploader.upload(file, public_id=filename)
                imagen = cloudinary.utils.cloudinary_url(filename)

                # si las validaciones no arrojan error se procede a enviar los datos a la base de datos
                status = ejercicios.actualizarEjercicio(
                    id, nombre, descripcion, imagen[0], tipo)
                return status
            else:
                return int(0)
        except Exception as error:
            print(error)

    def actualizarSinFoto(self, id, content):
        try:

            nombre = content['nombre']

            # se verifica que el nombre no este repetido en la base de datos
            verificarNombre = ejercicios.consultarEjercicioActualizar(nombre)

            # si el nombre esta repetido se envian string de esta forma se conoce el motivo

            if verificarNombre:
                status = "mal"
                return status

            # se verifica que el id enviado exista en la base de datos
            verificarId = ejercicios.ConsultaId(id)

            # si el len de verificarId es menor que 1 quiere decir que no existe este ejercicio en la base de datos
            if len(verificarId) < 1:
                status = False
                return status

            descripcion = content['descripcion']
            tipo = content['tipo']
            imagen = content['url']

            status = ejercicios.actualizarEjercicio(
                id, nombre, descripcion, imagen, tipo)
            return status
        except Exception as error:
            print(error)
