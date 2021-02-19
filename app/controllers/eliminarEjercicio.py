from app.model.model import Ejercicios
from app.controllers.consultaEjercicios import consulta

consultaEjercicios = consulta()

ejercicios = Ejercicios()

class Eliminar:

    def eliminar(self, id):
        
        consultar = ejercicios.ConsultaId(id)

        if len(consultar) > 0:
            ejercicios.remover(id)
            status = True
            return status
        else:
            status = False
            return status
