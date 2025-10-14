import mysql.connector

cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="12345678",
    database="uni")

# Get a cursor
cur = cnx.cursor()
query = "SELECT * from alumno"
query2 = "insert into alumno (nombre, apellido) values ('Juan', 'Perez')"
query3 = "delete from alumno where nombre='Tomas' and apellido='Castillo'"
query4 = "DELETE FROM `uni`.`curso` WHERE (`Id_Alumno` = '39') and (`Id_Materia` = '11'); DELETE FROM `uni`.`nota` WHERE (`Id_Nota` = '39'); DELETE FROM `uni`.`alumno` WHERE (`Id_Alumno` = '39');"
query5 = "update alumno set nombre='Fernanada', apellido='Castillo' where Id_Alumno=39"

#cur.execute(query4)
cur.execute(query5)

cur.execute(query)

for (nombre) in cur:
    print(nombre)
print(f"alumnos totales: {cur.rowcount}")


cur.close()
cnx.close()