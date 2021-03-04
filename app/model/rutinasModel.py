import psycopg2


class Rutinas:
    def registrar(self, id, nombre, descripcion, intensidad, dificultad, categoria):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "INSERT INTO rutinas VALUES (%s, %s, %s, %s, %s, %s)"
            datos = (id, nombre, descripcion,
                     intensidad, dificultad, categoria)

            cursor.execute(sql, datos)

            conexion.commit()

            status = True

        except Exception as error:
            print("Error in the conetion with the database", error)
            status = False

        finally:
            cursor.close()
            conexion.close()
            return status

# funcion encarga de consultar las rutinas dentro del sistema
    def consultar(self):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM rutinas ORDER BY id ASC"

            cursor.execute(sql,)
            diccionario = cursor.fetchall()
            diccionarios = []
            # se crea un objeto de items que luego se agrega a diccionarios
            for item in diccionario:
                items = {"id": item[0], "nombre": item[1], "descripcion": item[2],
                         "intensidad": item[3], "dificultad": item[4], "categoria": item[5]}

                diccionarios.append(items)
            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
            cursor.close()
            conexion.close()
            print(diccionarios)
            return diccionarios

# funcion que realiza una consulta a la asociacion de rutinas y ejercicios
    def consultaGeneral(self):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM rutinas ORDER BY id ASC"

            cursor.execute(sql,)
            diccionario = cursor.fetchall()
            diccionarios = []


# despues de consultar las rutinas se procede a consultar la asociacion entre estos
            for item in diccionario:
                try:
                    sql = "SELECT * FROM rutinasejercicio re, ejercicios e where re.idrutinas=%s AND e.id = re.idejercicio"
                    cursor.execute(sql, (item[0],))
                    ejercicio = cursor.fetchall()

                    # se crea un objeto de tipo items que recoje la informacion de la rutina
                    items = {"id": item[0], "nombre": item[1], "descripcion": item[2],
                             "intensidad": item[3], "dificultad": item[4], "categoria": item[5]}
                    ejercicios = []

                    # si hay ejercicios vinculados a la rutina se agregan a la informacion y se envia
                    for i in ejercicio:

                        ejer = {"idejercicio": i[0], "repeticiones": i[1], "series": i[2],
                                "ejecucion": i[3], "dia": i[4], "idrutinas": i[5], "nombre": i[7], "descripcion": i[8], "imagen": i[9], "tipo": i[10]}

                        ejercicios.append(ejer)

                        items["ejercicios"] = ejercicios

                except Exception as error:
                    print("Error in the conetion with the database", error)
                    pass

                diccionarios.append(items)

            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
            cursor.close()
            conexion.close()
            print(diccionarios)
            return diccionarios

    # funcion que recibe como parametros los ejercicios, y el id de la rutina para crear una relacion

    def registroEjercicios(self, ejercicios, id):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "INSERT INTO rutinasejercicio VALUES (%s, %s, %s, %s, %s, %s)"

            # se obtienen los datos de cada ejercicio para crear una relacion entre los ejercicios y las rutinas
            for i in ejercicios:
                id_ejercicio = i.get("id_ejercicio")
                repeticiones = i.get("repeticiones")
                series = i.get("series")
                ejecucion = i.get("ejecucion")
                dia = i.get("dia")

                datos = (id_ejercicio, repeticiones,
                         series, ejecucion, dia, id)

                cursor.execute(sql, datos)

                conexion.commit()

            status = True

        except Exception as error:
            print("Error in the conetion with the database", error)
            status = False

        finally:
            cursor.close()
            conexion.close()
            return status

    # funcion que consulta si el nombre de la rutina existe en la base de datos

    def consultarNombre(self, nombre):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM rutinas WHERE nombre = %s"

            cursor.execute(sql, (nombre,))
            diccionario = cursor.fetchall()
            conexion.commit()

            # si el len de diccionario es mayor a 0 indica que ya existe una rutina con este nombre
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

# se consulta en la bd que los ejercicios ha registrar existan en la base de datos
    def consultaIdEjercicio(self, ejercicios):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM ejercicios WHERE id = %s"

            diccionarios = list()

            # se verifica que el len de los ejercicios sea igual que el len de los ejercicios en la base de datos

            for i in ejercicios:
                id_ejercicio = i.get("id_ejercicio")

                cursor.execute(sql, (id_ejercicio,))
                diccionario = cursor.fetchall()
                conexion.commit()

                if len(diccionario) > 0:
                    diccionarios.append(diccionario)

            if len(diccionarios) == len(ejercicios):
                print(diccionarios, ejercicios)
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

    def asignarRutina(self, id, id_rutina):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "UPDATE usuarios SET id_rutina = %s WHERE id = %s"

            id = (id)
            id_rutina = (id_rutina)

            cursor.execute(sql, (id_rutina, id,))
            conexion.commit()
            status = True

        except Exception as error:
            print("Error in the conetion with the database", error)
            status = False

        finally:
            cursor.close()
            conexion.close()
            return status

# funcion que recibe el id del usuario para validar que este exista
    def usuario(self, id):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()
            sql = "SELECT * FROM usuarios WHERE id = %s"

            cursor.execute(sql, (id,))
            diccionario = cursor.fetchall()

# si el usuario existe se devuelve true
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

# funcion que recibe un id para verificar que la rutina exista
    def consultarId(self, id):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM rutinas WHERE id = %s"

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

# funcion que recibe un id de rutina para su posterior eliminacion
    def remover(self, id):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "DELETE FROM rutinas WHERE id= %s"

            cursor.execute(sql, (id,))

            conexion.commit()

        except Exception as error:
            print("Error in the connection with the database", error)

        finally:
            cursor.close()
            conexion.close()
