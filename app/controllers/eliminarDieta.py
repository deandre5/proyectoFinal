from app.model.dietasModel import Dietas

dietas = Dietas()

class EliminarDietas():

    def eliminar(self,id):

        consultar = dietas.consultarId(id)

        if consultar:
            dietas.remover(id)
            status = True
            return status
        
        else:
            status = False
            return status

