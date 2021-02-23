from app.model.ejerciciosModel import Ejercicios


ejercicios = Ejercicios()



class consulta:

#metodo encargado de realizar la consulta general de los ejercicios
    def consultar(self):
       
        diccionario = ejercicios.consultar()
        return diccionario

#metodo encargado de recibir y enviar al model el id del ejercicio a consultar
    def consultaID(self, id):
        #recibe la informacion a consultar y la devuelve
        diccionario = ejercicios.ConsultaId(id)
        return diccionario
    
    
