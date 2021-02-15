import psycopg2


class Ejercicios:
    def consultar(self):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")
            cursor = conexion.cursor()

            sql = "SELECT * FROM ejercicios"
            cursor.execute(sql)
            diccionario = cursor.fetchall()
            diccionarios = []
            for item in diccionario:
                items={"id": item[0], "nombre": item[1], "descripcion": item[2], "imagen": item[3], "tipo": item[4]}

                diccionarios.append(items)
            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
            cursor.close()
            conexion.close()
            print(diccionarios)
            return diccionarios

    # se encarga de crear una conexion con la base de datos y mediante el id recibir toda la informacion del ejercicio
    def ConsultaId(self, id):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")
            cursor = conexion.cursor()

            sql = "SELECT * FROM ejercicios WHERE id = %s"
            cursor.execute(sql, (id))
            diccionario = cursor.fetchall()
            diccionarios = []
            for item in diccionario:
                items={"id": item[0], "nombre": item[1], "descripcion": item[2], "imagen": item[3], "tipo": item[4]}

            diccionarios.append(items)

            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
            print(diccionarios)
            cursor.close()
            conexion.close()
            return diccionarios
