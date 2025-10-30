import mysql.connector
import carrera as c
lista = []
def connect_db(user,passwd):
    try:
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user= user,
            password= passwd,
            database="carreras")
        return cnx
    except mysql.connector.Error as err:
        return err

def añadir_carrera(cur,nueva_carrera):
    try:
        cur.execute("INSERT INTO carrera (Nombre_Carrera,Nota_de_corte,Duracion) VALUES (%s,%s,%s)", (nueva_carrera.getter(),nueva_carrera.get_nota_corte(),nueva_carrera.get_duracion(),))
    except mysql.connector.Error as err:
        print("Error al insertar la carrera (añadir_carrera):", err)
        
def modificar_carrera(cur, id_carrera, nombre_carrera, nota_corte, duracion):
    try:
        cur.execute("UPDATE carrera SET Nombre_Carrera=%s, Nota_de_corte=%s, Duracion=%s WHERE Id_Carrera=%s",(nombre_carrera, nota_corte, duracion, id_carrera))
        return cur.rowcount
    except mysql.connector.Error as err:
        print(f"Error al modificar la carrera: {err}")
        return 0


def ver_carreras(cur):
    import carrera as c
    try:
        cur.execute("SELECT * FROM carrera")
        filas = cur.fetchall()
        lista_carreras = []
        for f in filas:
            carrera_obj = c.carrera(
                nombre_carrera=f['Nombre_Carrera'],
                id_carrera=f['Id_Carrera'],
                nota_corte=f['Nota_de_corte'],
                duracion=f['Duracion']
            )
            lista_carreras.append(carrera_obj)
        return lista_carreras
    except mysql.connector.Error as err:
        print("Error al ver las carreras:", err)
        return []
        
def borrar_carrera(cursor,borrar_carrera): 
    try:         
        cursor.execute("SELECT Nombre_Carrera FROM carrera WHERE id_Carrera = %s", (borrar_carrera.get_id_carrera(),))
        resultados = cursor.fetchall()
        cursor.execute("DELETE from carrera WHERE id_Carrera = %s", (borrar_carrera.get_id_carrera(),))
        return resultados
    except mysql.connector.Error as err:
        print("Error al borrar la carrera: ",err)  