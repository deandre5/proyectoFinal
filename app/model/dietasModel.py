import psycopg2

class Dietas:

    def consultaNombre(self, nombre):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM dietas WHERE nombre = %s"

            cursor.execute(sql, (nombre,))
            diccionario = cursor.fetchall()
            conexion.commit()

            print(diccionario)

            # se examina el len del diccionario despues de la consulta, si es mayor a cero se devuelve true ya que se encuentra repetido

            if len(diccionario) > 0:
                status = True
            # caso contrario false
            else:
                status = False

        except Exception as error:
            print("Error in the conetion with the database", error)

            status = False

        finally:

            cursor.close()
            conexion.close()
            return status


    def consultar(self):
        try:

            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")
            cursor = conexion.cursor()

            sql = "SELECT * FROM dietas ORDER BY id ASC"
            cursor.execute(sql)
            diccionario = cursor.fetchall()
            diccionarios = []
            # for que nos permite crear un objeto items para luego añadirlo a una lista y devolver su contenido
            for item in diccionario:
                items = {"id": item[0], "nombre": item[1],
                         "categoria": item[2], "descripcion": item[3]}

                diccionarios.append(items)
            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
            cursor.close()
            conexion.close()
            print(diccionarios)
            return diccionarios


    def registro(self, id_bd, nombre, categoria, descripcion):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "INSERT INTO dietas VALUES(%s, %s, %s, %s)"
            datos = (id_bd, nombre, categoria, descripcion)

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

    
    def ConsultaId(self, id):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")
            cursor = conexion.cursor()

            sql = "SELECT * FROM dietas WHERE id = %s"
            cursor.execute(sql, (id, ))
            diccionario = cursor.fetchall()
            diccionarios = []
            # for que nos permite crear un objeto items para luego añadirlo a una lista y devolver su contenido
            for item in diccionario:
                items = {"id": item[0], "nombre": item[1],
                         "categoria": item[2], "descripcion": item[3]}

            diccionarios.append(items)

            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
            print(diccionarios)
            cursor.close()
            conexion.close()
            return diccionarios


    def consultarId(self, id):
        print("*-*-*-*-*-*-*",id)
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM dietas WHERE id = %s"

            cursor.execute(sql, (id,))
            diccionario = cursor.fetchall()
            conexion.commit()

            print(diccionario)
            # si la rutina existe se devuelve true
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

    def asignarDieta(self, id, idDieta):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "UPDATE personas SET iddieta = %s WHERE documento = %s"

            id = (id)
            idDieta = (idDieta)

            cursor.execute(sql, (idDieta, id,))
            conexion.commit()
            status = True

        except Exception as error:
            print("Error in the conetion with the database", error)
            status = False

        finally:
            cursor.close()
            conexion.close()
            return status