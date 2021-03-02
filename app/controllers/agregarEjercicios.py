from app.model.ejerciciosModel import Ejercicios


ejercicios = Ejercicios()


class agregar():

    # metodo que extrae la informacion del json, luego consulta que el nombre no exista y envia a la bd
    def agregarEjercicios(self, nombre, descripcion, tipo, filename):
        try:
            nombre = str(nombre)
            descripcion = str(descripcion)
            imagen = str(filename)
            print("------",imagen)
            tipo = str(tipo)

            consulta = ejercicios.consultar()

            if consulta:
                for i in consulta:
                    id_bd = i.get('id')+1
            else:
                id_bd = 1

            status = ejercicios.insert(
                id_bd, nombre, descripcion, imagen, tipo)
            return status
        except Exception as error:
            print(error)
            status = False
            return status

    def consultar(self, nombre):
        nombre = str(nombre)

        status = ejercicios.consultarEjercicio(nombre)
        return status
