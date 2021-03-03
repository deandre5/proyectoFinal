from app.model.ejerciciosModel import Ejercicios


ejercicios = Ejercicios()


class ActualizarEjercicios:

    def actualizar(self, nombre, descripcion,tipo, id, filename):

        try:
            nombre = str(nombre)
            descripcion = str(descripcion)
            imagen = str(filename)
            tipo = str(tipo)

            verificarId = ejercicios.ConsultaId(id)

            verificarNombre = ejercicios.consultarEjercicioActualizar(nombre)

            if verificarNombre:
                status = "mal"
                return status

            if len(verificarId) < 1:
                status = False
                return status

            status = ejercicios.actualizarEjercicio(
                id, nombre, descripcion, imagen, tipo)
            return status
        except Exception as error:
            print(error)
