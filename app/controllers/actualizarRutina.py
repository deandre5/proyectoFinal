from app.model.rutinasModel import Rutinas

rutinas = Rutinas()

class ActualizarRutina():
    def actualizarRutina(self, content, id):
        try:
            nombre = content.get('nombre')
            descripcion = content.get('descripcion')
            intensidad = content.get('intensidad')
            dificultad = content.get('dificultad')
            categoria = content.get('categoria')
            ejercicios = content.get('ejercicios')

            print(ejercicios)

            consultaIDEjercicios = rutinas.consultaIdEjercicio(ejercicios)

            if consultaIDEjercicios:
                
                actualizar = rutinas.actualizar(id,nombre, descripcion, intensidad, dificultad, categoria)
                

                if actualizar:

                    status = rutinas.ActualizacionEjercicios(id, ejercicios)


                    return status
                else:
                    status = "MAL"
                    return status

        except Exception as error:
            print(error)
            status = False
            return status