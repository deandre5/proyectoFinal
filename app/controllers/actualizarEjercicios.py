from app.model.ejerciciosModel import Ejercicios


ejercicios = Ejercicios()


class ActualizarEjercicios:

    # funcion que recibe los datos del ejercicio a actualizar
    def actualizar(self, nombre, descripcion, tipo, id, filename):

        try:
            nombre = str(nombre)
            descripcion = str(descripcion)
            imagen = str(filename)
            tipo = str(tipo)

            # se verifica que el id enviado exista en la base de datos
            verificarId = ejercicios.ConsultaId(id)

            # se verifica que el nombre no este repetido en la base de datos
            verificarNombre = ejercicios.consultarEjercicioActualizar(nombre)

            # si el nombre esta repetido se envian string de esta forma se conoce el motivo
            if verificarNombre:
                status = "mal"
                return status

            # si el len de verificarId es menor que 1 quiere decir que no existe este ejercicio en la base de datos
            if len(verificarId) < 1:
                status = False
                return status

            # si las validaciones no arrojan error se procede a enviar los datos a la base de datos
            status = ejercicios.actualizarEjercicio(
                id, nombre, descripcion, imagen, tipo)
            return status
        except Exception as error:
            print(error)
