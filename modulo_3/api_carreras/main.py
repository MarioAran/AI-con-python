import json
import requests as req
import os
import sys
import time
import flask 
VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
AZUL = "\033[94m"
NEGRITA = "\033[1m"
RESET = "\033[0m"

API_BASE = "http://localhost:5000"

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    input(f"\n{AZUL}Presiona ENTER para continuar...{RESET}")

def mostrar_menu():
    print(f"""{NEGRITA}
=============================
     GESTOR DE CARRERAS
=============================
{RESET}
1. Añadir carrera
2. Actualizar carrera
3. Ver carreras
4. Borrar carrera
5. Salir
=============================""")

def comprobar_conexion():
    try:
        req.get(API_BASE + "/", timeout=3)
        return True
    except req.exceptions.RequestException:
        print(f"{ROJO}No se pudo conectar con el servidor Flask. Asegúrate de que esté ejecutándose.{RESET}")
        return False

def input_numerico(mensaje, tipo=int, minimo=None, maximo=None):
    intentos = 0
    while True:
        valor = input(mensaje).strip()
        try:
            if tipo == int:
                valor = int(valor)
            else:
                valor = float(valor)
            if minimo is not None and valor < minimo:
                print(f"{AMARILLO}El valor debe ser mayor o igual que {minimo}.{RESET}")
                continue
            if maximo is not None and valor > maximo:
                print(f"{AMARILLO}El valor debe ser menor o igual que {maximo}.{RESET}")
                continue
            return valor
        except ValueError:
            intentos +=1
            print(f"{ROJO}Entrada inválida. Introduce un número válido.{RESET}")
            if intentos >=3:
                break
    
def añadir_carrera():
    print(f"\n{NEGRITA}--- AÑADIR CARRERA ---{RESET}")
    nombre = input("Nombre de la carrera: ")
    duracion = input_numerico("Duración (en años): ", tipo=int, minimo=1)
    nota_corte = input_numerico("Nota de corte (0 - 14): ", tipo=float, minimo=0, maximo=14)
    payload = {"nombre": nombre, "duracion": duracion, "nota_corte": nota_corte}
    try:
        response = req.post(f"{API_BASE}/agregar/carrera/", json=payload, timeout=5)
    except req.exceptions.RequestException:
        print(f"{ROJO}Error: No se pudo conectar con el servidor.{RESET}")
        return
    if response.status_code == 201:
        print(f"\n{VERDE}Carrera '{nombre}' añadida correctamente.{RESET}")
    else:
        print(f"\n{ROJO}Error: {response.text}{RESET}")

def actualizar_carrera():
    print(f"\n{NEGRITA}--- ACTUALIZAR CARRERA ---{RESET}")
    id_carrera = input_numerico("ID de la carrera a actualizar: ", tipo=int, minimo=1)
    nombre = input("Nuevo nombre: ").strip()
    duracion = input_numerico("Nueva duración (en años): ", tipo=int, minimo=1)
    nota_corte = input_numerico("Nueva nota de corte (0 - 14): ", tipo=float, minimo=0, maximo=14)
    payload = {"nombre": nombre, "duracion": duracion, "nota_corte": nota_corte}
    try:
        response = req.put(f"{API_BASE}/actualizar/carrera/{id_carrera}", json=payload, timeout=5)
    except req.exceptions.RequestException:
        print(f"{ROJO}Error: No se pudo conectar con el servidor.{RESET}")
        return
    if response.status_code == 200:
        print(f"\n{VERDE}Carrera '{nombre}' actualizada correctamente.{RESET}")
    elif response.status_code == 404:
        print(f"\n{AMARILLO}Carrera no encontrada.{RESET}")
    else:
        print(f"\n{ROJO}Error: {response.text}{RESET}")

def ver_carreras():
    print(f"\n{NEGRITA}--- LISTA DE CARRERAS ---{RESET}")
    try:
        response = req.get(f"{API_BASE}/ver/carreras/", timeout=5)
    except req.exceptions.RequestException:
        print(f"{ROJO}Error: No se pudo conectar con el servidor.{RESET}")
        return
    if response.status_code == 200:
        try:
            
            data = response.json()
        except json.JSONDecodeError as err:
            print(f"{ROJO}Error: respuesta no válida del servidor.{RESET}")
        if not data:
            print(f"{AMARILLO}No hay carreras registradas.{RESET}")
        else:
            print(f"\n{AZUL}Total: {len(data)} carreras registradas.{RESET}\n")
            for c in data:
                print(f"[{c['Id_Carrera']}] {NEGRITA}{c['Nombre_Carrera']}{RESET} "
                      f"({c['Duracion']} años) - Nota: {c['Nota_de_corte']}")
            print(f"\n{AZUL}--- JSON completo ---{RESET}\n")
            #print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print(f"{ROJO}Error al obtener las carreras.{RESET}")

def borrar_carrera():
    print(f"\n{NEGRITA}--- BORRAR CARRERA ---{RESET}")
    id_carrera = input_numerico("ID de la carrera a borrar: ", tipo=int, minimo=1)
    confirmacion = input(f"{AMARILLO}¿Seguro que quieres borrar la carrera con ID {id_carrera}? (s/n): {RESET}").lower()
    if confirmacion != 's':
        print("Operación cancelada.")
        return
    try:
        response = req.delete(f"{API_BASE}/borrar/carrera/{id_carrera}", timeout=5)
    except req.exceptions.RequestException:
        print(f"{ROJO}Error: No se pudo conectar con el servidor.{RESET}")
        return
    if response.status_code == 200:
        print(f"{VERDE}{response.json()['mensaje']}{RESET}")
    elif response.status_code == 404:
        print(f"{AMARILLO}Carrera no encontrada.{RESET}")
    else:
        print(f"{ROJO}Error: {response.text}{RESET}")

def main():
    if not comprobar_conexion():
        sys.exit()
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input(f"{AZUL}Selecciona una opción: {RESET}").strip()
        if opcion == "1":
            limpiar_pantalla()
            ver_carreras()
            añadir_carrera()
            pausa()
        elif opcion == "2":
            limpiar_pantalla()
            ver_carreras()
            actualizar_carrera()
            pausa()
        elif opcion == "3":
            limpiar_pantalla()
            ver_carreras()
            pausa()
        elif opcion == "4":
            limpiar_pantalla()
            ver_carreras()
            borrar_carrera()
            pausa()

        elif opcion == "5":
            print(f"\n{VERDE}Saliendo del programa...{RESET}\n")
            time.sleep(1)
            break
        else:
            print(f"{AMARILLO}Opción no válida.{RESET}")
            pausa()

if __name__ == "__main__":
    main()
