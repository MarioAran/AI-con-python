import requests as req
usuario = input("ingrese el usuario: ")
contraseña = input("ingrese la contraseña: ")
datos = {'user':usuario,'passwd':contraseña}
resp = req.post("http://127.0.0.1:5000/guardar/", data=datos)
print(resp.content)
