from app.model.model import Ejercicios


ejercicios = Ejercicios()

class agregar():

    def agregarEjercicios(self, content):
        try:
            nombre = str(content.get('nombre'))
            descripcion = str(content.get('descripcion'))
            imagen = str(content.get('imagen'))
            tipo = str(content.get('tipo'))

            consulta = ejercicios.consultar()

            if consulta:
                for i in consulta:
                    id_bd = i.get('id')+1
            else:
                id_bd = 1

            status = ejercicios.insert(id_bd, nombre, descripcion, imagen, tipo)
            return status
        except Exception as error:
            print(error)
            status = False
            return status

    def consultar(self, content):
        nombre = str(content.get('nombre'))
        

        status = ejercicios.consultarEjercicio(nombre)
        return status