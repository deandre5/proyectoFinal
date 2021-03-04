from app.model.rutinasModel import Rutinas

rutinas = Rutinas()


class Asignar():

    # funcion que recibe el id de la rutina y el id del usuario
    def asignar(id, id_rutina):

        # se envia el id del usuario para validar que este exista en la base de datos
        usuario = rutinas.usuario(id)

        if usuario:
            # se envia el id de la rutina para validar que exista
            rutina = rutinas.consultarId(id_rutina)

            if rutina:
                # si ambas validaciones son correctas se procede a realizar la asignacion de rutina al usuario
                status = rutinas.asignarRutina(id, id_rutina)
                return status

            # si la rutina no existe se devuelve un string
            else:
                status = "MAL"
                return status

        else:
            status = False
            return status
