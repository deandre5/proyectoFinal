import psycopg2


class Ejercicios:
    def consultar(self):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")
            cursor = conexion.cursor()

            sql = "SELECT * FROM ejercicios ORDER BY id ASC"
            cursor.execute(sql)
            diccionario = cursor.fetchall()
            diccionarios = []
            for item in diccionario:
                items = {"id": item[0], "nombre": item[1],
                         "descripcion": item[2], "imagen": str(item[3]), "tipo": item[4]}

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
            cursor.execute(sql, (id, ))
            diccionario = cursor.fetchall()
            diccionarios = []
            for item in diccionario:
                items = {"id": item[0], "nombre": item[1],
                         "descripcion": item[2], "imagen": str(item[3]), "tipo": item[4]}

            diccionarios.append(items)

            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
            print(diccionarios)
            cursor.close()
            conexion.close()
            return diccionarios

    def insert(self, id, nombre, descripcion, imagen, tipo):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            imagen = ('https://proyectofinalsena.herokuapp.com/app/static/'+imagen)
            sql = "INSERT INTO ejercicios VALUES(%s, %s, %s, %s, %s)"
            datos = (id, nombre, descripcion, imagen, tipo)

            cursor.execute(sql, datos)

            conexion.commit()

            status = True

        except Exception as error:
            print("Error in the conexion with the database", error)

            status = False

        finally:
            cursor.close()
            conexion.close()
            return status

    def consultarEjercicio(self, nombre):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM ejercicios WHERE nombre = %s"

            cursor.execute(sql, (nombre,))
            diccionario = cursor.fetchall()
            conexion.commit()

            print(diccionario)

            if len(diccionario) > 0:
                status = True
            else:
                status = False

        except Exception as error:
            print("Error in the conetion with the database", error)

            status = False

        finally:

            cursor.close()
            conexion.close()
            return status

    def actualizarEjercicio(self, id, nombre, descripcion, imagen, tipo):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "UPDATE ejercicios SET nombre = %s, descripcion = %s, imagen = %s, tipo = %s WHERE id = %s "

            id = (id)
            nombre = (nombre)
            descripcion = (descripcion)
            imagen = ('https://proyectofinalsena.herokuapp.com/static/'+imagen)
            tipo = (tipo)

            cursor.execute(sql, (nombre, descripcion, imagen, tipo, id))
            conexion.commit()
            status = True

        except Exception as error:
            print("Error in the conetion with the database", error)
            status = False
        finally:
            cursor.close()
            conexion.close()
            return status

    def remover(self, id):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "DELETE FROM ejercicios WHERE id = %s"

            cursor.execute(sql, (id,))

            conexion.commit()

        except Exception as error:
            print("Error in the connection with the database", error)

        finally:
            cursor.close()
            conexion.close()
