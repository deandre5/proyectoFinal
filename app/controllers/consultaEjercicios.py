from app.model.model import Ejercicios


ejercicios = Ejercicios()


#metodo encargado de recibir y enviar al model el id del ejercicio a consultar
class consulta:

    def consultar(self):
       
        diccionario = ejercicios.consultar()
        return diccionario

    def consultaID(self, id):
        #recibe la informacion a consultar y la devuelve
        diccionario = ejercicios.ConsultaId(id)
        return diccionario
    
    
