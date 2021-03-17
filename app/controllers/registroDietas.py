from app.model.dietasModel import Dietas

dietas = Dietas()

class AgregarDietas():

    def agregarDieta(self, content):
        try:
            nombre = content.get('nombre')
            categoria = content.get('categoria')
            descripcion = content.get('descripcion')

            consultaNombre = dietas.consultaNombre(nombre)

            if consultaNombre:
                return 'MAL'

            consulta = dietas.consultar()

            # si hay ejercicios registrados se toma el ultimo y se le suma 1 al id, luego se toma este id y se envia para el registro del ejercicio
            if consulta:
                for i in consulta:
                    id_bd = i.get('id')+1
            # si no hay ejercicios registrados, este toma el valor de 1
            else:
                id_bd = 1

            status = dietas.registro(id_bd, nombre, categoria, descripcion)

            return status
        
        except Exception as error:
            print(error)
            status = False
            return status

    
