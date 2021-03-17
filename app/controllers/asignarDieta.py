from app.model.dietasModel import Dietas
from app.model.rutinasModel import Rutinas


rutinas = Rutinas()
dietas = Dietas()

class AsignarDietas():

    def asignar(self, idDieta, id):
        print(id,"*-*-*-*-*-*")
        print(idDieta,"*-*-*-*-*")
        # se envia el id del usuario para validar que este exista en la base de datos
        usuario = rutinas.usuario(id)

        if usuario:
            # se envia el id de la rutina para validar que exista
            dieta = dietas.consultarId(idDieta)

            if dieta:
                # si ambas validaciones son correctas se procede a realizar la asignacion de rutina al usuario
                status = dietas.asignarDieta(id, idDieta)
                return status

            # si la rutina no existe se devuelve un string
            else:
                status = "MAL"
                return status

        else:
            status = False
            return status