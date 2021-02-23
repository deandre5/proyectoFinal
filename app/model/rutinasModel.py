import psycopg2


class Rutinas:
    def registrar(self, id, nombre, descripcion, intensidad, dificultad, categoria):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "INSERT INTO rutinas VALUES (%s, %s, %s, %s, %s, %s)"
            datos = (id, nombre, descripcion, intensidad, dificultad, categoria)

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

    def consultar(self):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM rutinas ORDER BY id ASC"

            cursor.execute(sql,)
            diccionario = cursor.fetchall()
            diccionarios = []
            for item in diccionario:
                items={"id": item[0], "nombre": item[1], "descripcion": item[2], "intensidad": item[3], "dificultad": item[4], "categoria": item[5]}

                diccionarios.append(items)
            conexion.commit()

        except Exception as error:
            print("Error in the conetion with the database", error)
        finally:
            cursor.close()
            conexion.close()
            print(diccionarios)
            return diccionarios

    def registroEjercicios(self, ejercicios, id):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "INSERT INTO rutinasejercicio VALUES (%s, %s, %s, %s, %s, %s)"

            for i in ejercicios:
                id_ejercicio = i.get("id_ejercicio")
                repeticiones = i.get("repeticiones")
                series = i.get("series")
                ejecucion = i.get("ejecucion")
                dia = i.get("dia")

                datos = ( id_ejercicio, repeticiones, series, ejecucion, dia, id)

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


    def consultarNombre(self,nombre):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM rutinas WHERE nombre = %s"


            cursor.execute(sql,(nombre,))
            diccionario = cursor.fetchall()
            conexion.commit()

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

    def consultaIdEjercicio(self,ejercicios):
        try:
            conexion = psycopg2.connect(database="dd1o1liu6nsqob", user="gvjdpzhyjsvfxs", password="5ffbbd36b7bf7d3ff6e7edb572b8667da3b15d4396b445f4e705f13c25f8d075",
                                        host="ec2-52-23-190-126.compute-1.amazonaws.com", port="5432")

            cursor = conexion.cursor()

            sql = "SELECT * FROM ejercicios WHERE id = %s"

            diccionarios = list()
            
            for i in ejercicios:
                id_ejercicio = i.get("id_ejercicio")

                cursor.execute(sql,(id_ejercicio,))
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
