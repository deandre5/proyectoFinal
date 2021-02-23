from app.model.rutinasModel import Rutinas

rutinas = Rutinas()


class AgregarRutina():

    def agregar(self, content):

        try:

            nombre = content.get('nombre')
            descripcion = content.get('descripcion')
            intensidad = content.get('intensidad')
            dificultad = content.get('dificultad')
            categoria = content.get('categoria')
            ejercicios = content.get('ejercicios')

            consultaIDEjercicios = rutinas.consultaIdEjercicio(ejercicios)

            print(consultaIDEjercicios)

            if consultaIDEjercicios:

                consulta = rutinas.consultar()

                if consulta:
                    for i in consulta:
                        id_bd = i.get('id')+1
                else:
                    id_bd = 1

                registro = rutinas.registrar(
                    id_bd, nombre, descripcion, intensidad, dificultad, categoria)

                if registro:

                    status = rutinas.registroEjercicios(ejercicios, id_bd)

                    return status
            else:
                status = "MAL"
                return status

        except Exception as error:
            print (error)
            status = False
            return status


    def consulta(self, content):
        nombre = content.get('nombre')

        status = rutinas.consultarNombre(nombre)
        return status
