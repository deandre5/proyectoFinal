from app.model.rutinasModel import Rutinas

rutinas = Rutinas()


class Asignar():

    def asignar(id, id_rutina):

        print(id, id_rutina)

        usuario = rutinas.usuario(id)

        if usuario:

            rutina = rutinas.consultarId(id_rutina)

            if rutina:

                status = rutinas.asignarRutina(id, id_rutina)
                return status

            else:
                status = "MAL"
                return status

        else:
            status = False
            return status
