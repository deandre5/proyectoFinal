from app.model.dietasModel import Dietas

dietas = Dietas()

class ActualizarDieta():

    def actualizar(self,id,content):
        try:
            nombre = content.get('nombre')
            categoria = content.get('categoria')
            descripcion = content.get('descripcion')

            verificarId = dietas.ConsultaId(id)

            verificarNombre = dietas.consultarDietaActualizar(nombre)

            if verificarNombre:
                status = "mal"
                return status

            # si el len de verificarId es menor que 1 quiere decir que no existe este ejercicio en la base de datos
            if len(verificarId) < 1:
                status = False
                return status

            status = dietas.actualizarDietas(
                id, nombre, categoria, descripcion)
            return status

        except Exception as error:
            print(error)