from app.model.rutinasModel import Rutinas

rutinas = Rutinas()


class consultarRutinas():
    # funcion que controla la consulta a la asociacion de rutinas y ejercicios
    def consultar(self):
        diccionario = rutinas.consultaGeneral()
        return diccionario
