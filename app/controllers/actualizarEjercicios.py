from app.model.ejerciciosModel import Ejercicios


ejercicios = Ejercicios()

class ActualizarEjercicios:

    def actualizar(self, content, id):

        try:
            nombre = content.get('nombre')
            descripcion = content.get('descripcion')
            imagen = content.get('imagen')
            tipo = content.get('tipo')

            

            verificarId = ejercicios.ConsultaId(id)
           
            verificarNombre = ejercicios.consultarEjercicio(nombre)
            

            if verificarNombre:
                status = "mal"
                return status

            

            if len(verificarId) < 1:
                status = False
                return status

            status = ejercicios.actualizarEjercicio(id, nombre, descripcion, imagen, tipo)
            return status
        except Exception as error:
            print (error)