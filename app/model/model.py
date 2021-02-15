import psycopg2

class Ejercicios:
    def consultar(self):
        try:
            conexion = psycopg2.connect(database="ProyectoFinal", user="postgres", password="SCOOBy0306@")
            cursor = conexion.cursor()

            sql = "SELECT * FROM ejercicios"
            cursor.execute(sql)
            diccionario = cursor.fetchall()

            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
           cursor.close()
           conexion.close()
           return diccionario

    #se encarga de crear una conexion con la base de datos y mediante el id recibir toda la informacion del ejercicio
    def ConsultaId(self, id):
        try:
            conexion = psycopg2.connect(database="ProyectoFinal", user="postgres", password="SCOOBy0306@")
            cursor = conexion.cursor()

            sql = "SELECT * FROM ejercicios WHERE id = %s"
            cursor.execute(sql, (id))
            diccionario = cursor.fetchall()

            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
           cursor.close()
           conexion.close()
           return diccionario