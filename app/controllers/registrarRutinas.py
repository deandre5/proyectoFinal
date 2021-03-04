from app.model.rutinasModel import Rutinas

rutinas = Rutinas()


class AgregarRutina():
    # funcion que recibe el json, lo separa en variables y lo envia para su registro
    def agregar(self, content):

        try:

            nombre = content.get('nombre')
            descripcion = content.get('descripcion')
            intensidad = content.get('intensidad')
            dificultad = content.get('dificultad')
            categoria = content.get('categoria')
            ejercicios = content.get('ejercicios')

            # se consulta en la base de datos que los ejercicios existan
            consultaIDEjercicios = rutinas.consultaIdEjercicio(ejercicios)

    # si los ejercicios existene en la base de datos se procede a darle un id a la rutina para su registro en la base de datos
            if consultaIDEjercicios:

                consulta = rutinas.consultar()
                # si hay mas ejercicios registrados se le asigna el ultimo id + 1, si no hay ejercicios se le asigna el 1
                if consulta:
                    for i in consulta:
                        id_bd = i.get('id')+1
                else:
                    id_bd = 1

                registro = rutinas.registrar(
                    id_bd, nombre, descripcion, intensidad, dificultad, categoria)

                # si el registo de la rutinas es exitoso se procede a crear una relacion entre la rutina y los ejercicios
                if registro:

                    status = rutinas.registroEjercicios(ejercicios, id_bd)

                    return status
            else:
                # si no existen los ejercicios se devuelve un string avisandole al sistema de esto
                status = "MAL"
                return status

        except Exception as error:
            print(error)
            status = False
            return status

# funcion que recibe el json y envia el nombre de la rutina para verificar si ya existe en la base de datos
    def consulta(self, content):
        nombre = content.get('nombre')

        status = rutinas.consultarNombre(nombre)
        return status
