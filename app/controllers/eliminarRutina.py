from app.model.rutinasModel import Rutinas

rutinas = Rutinas()


class eliminar:
    # funcion que recibe el id de la rutina
    def eliminarRutina(id):

        # se valida que la rutina exista
        consulta = rutinas.consultarId(id)

    # si la validacion es correcta se procede a la eliminacion, caso contrario se devuelve false
        if consulta:
            rutinas.remover(id)
            status = True
            return status
        else:
            status = False
            return status
