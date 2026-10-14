"""
Cliente en consola para interactuar con la API de tareas.
"""
import requests

BASE_URL = "http://localhost:5000"

def registrar():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    r = requests.post(f"{BASE_URL}/registro", 
                      json={"usuario": usuario, "contraseña": contraseña})
    print(r.json())

def login():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    r = requests.post(f"{BASE_URL}/login", 
                      json={"usuario": usuario, "contraseña": contraseña})
    print(r.json())

def ver_tareas():
    r = requests.get(f"{BASE_URL}/tareas")
    print(r.text)

def main():
    while True:
        print("\n--- Menú ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Ver tareas (HTML)")
        print("4. Salir")
        opcion = input("Seleccione: ")
        
        if opcion == "1": registrar()
        elif opcion == "2": login()
        elif opcion == "3": ver_tareas()
        elif opcion == "4": break
        else: print("Opción inválida")

if __name__ == "__main__":
    main()