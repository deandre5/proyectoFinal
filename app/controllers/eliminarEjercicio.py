from app.model.ejerciciosModel import Ejercicios
from app.controllers.consultaEjercicios import consulta

consultaEjercicios = consulta()

ejercicios = Ejercicios()


class Eliminar:

    # funcion que recibe un id del ejercicio verifica que existe y luego lo elimina de la base de datos
    def eliminar(self, id):

        # consulta que el id exista
        consultar = ejercicios.ConsultaId(id)

        # si el id existe se procede a removerlo de la base de datos y enviar un status true
        if len(consultar) > 0:
            ejercicios.remover(id)
            status = True
            return status

        # si el id no existe devuelve false
        else:
            status = False
            return status
