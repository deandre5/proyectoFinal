from app.model.dietasModel import Dietas

dietas = Dietas()

class ConsultaDietas:
    def consulta(self):
        diccionario = dietas.consultar()
        return diccionario

    def consultaID(self, id):

        diccionario = dietas.ConsultaId(id)
        return diccionario