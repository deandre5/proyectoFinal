from app.model.rutinasModel import Rutinas

rutinas = Rutinas()

class eliminar:

    def eliminarRutina( id):
        
        consulta = rutinas.consultarId(id)

        if consulta:
            rutinas.remover(id)
            status = True
            return status
        else:
            status = False
            return status