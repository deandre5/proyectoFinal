from app.model.ejerciciosModel import Ejercicios


ejercicios = Ejercicios()


class agregar():

    # metodo que recibe la informacion del ejercicio para su registro
    def agregarEjercicios(self, nombre, descripcion, tipo, filename):
        try:
            nombre = str(nombre)
            descripcion = str(descripcion)
            imagen = str(filename)

            tipo = str(tipo)

            # se consultan todos los ejercicios, despues de esto se le asigna el id al ejercicio
            consulta = ejercicios.consultar()

            # si hay ejercicios registrados se toma el ultimo y se le suma 1 al id, luego se toma este id y se envia para el registro del ejercicio
            if consulta:
                for i in consulta:
                    id_bd = i.get('id')+1
            # si no hay ejercicios registrados, este toma el valor de 1
            else:
                id_bd = 1

            # se envian los datos a la base de datos  para su registro y se devuelve la respuesta
            status = ejercicios.insert(
                id_bd, nombre, descripcion, imagen, tipo)
            return status
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
