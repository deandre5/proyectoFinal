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


class agregar():

    # metodo que recibe la informacion del ejercicio para su registro
    def agregarEjercicios(self,content, file):
        try:
            
            
            # se consultan todos los ejercicios, despues de esto se le asigna el id al ejercicio
            consulta = ejercicios.consultar()

            # si hay ejercicios registrados se toma el ultimo y se le suma 1 al id, luego se toma este id y se envia para el registro del ejercicio
            if consulta:
                for i in consulta:
                    id_bd = i.get('id')+1
            # si no hay ejercicios registrados, este toma el valor de 1
            else:
                id_bd = 1


            if allowed_file(file.filename):

                descripcion = content['descripcion']
                tipo = content['tipo']
                nombre = content['nombre']


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

                # se envian los datos a la base de datos  para su registro y se devuelve la respuesta
                status = ejercicios.insert(
                id_bd, nombre, descripcion, imagen[0], tipo)
                return status
            else:
                return int(0)
        except Exception as error:
            print(error)
            status = False
            return status

    # funcion que recibe el nombre del ejercicio, luego se envia a la base de datos
    def consultar(self, nombre):
        nombre = str(nombre)

        # si el nombre esta registrado obtiene true y devuelve a la base de datos
        status = ejercicios.consultarEjercicio(nombre)
        return status
