import os
import csv
import sys

def obtener_directorio_script():
    """Obtiene el directorio del script actual."""
    return os.path.dirname(os.path.abspath(__file__))

def cargar_empleados():
    """Carga los empleados desde el archivo CSV."""
    empleados = {}
    archivo_path = os.path.join(obtener_directorio_script(), "empleados.csv")
    if os.path.exists(archivo_path):
        with open(archivo_path, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                empleados[fila["cedula"]] = fila
    return empleados

def guardar_empleados(empleados):
    """Guarda la lista de empleados en un archivo CSV."""
    archivo_path = os.path.join(obtener_directorio_script(), "empleados.csv")
    with open(archivo_path, "w", newline="", encoding="utf-8") as archivo:
        campos = ["cedula", "nombres", "apellidos"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for empleado in empleados.values():
            escritor.writerow(empleado)

def agregar_empleado(empleados):
    """Solicita y agrega un nuevo empleado al diccionario de empleados."""
    cedula = input("Ingrese cédula = ").strip()
    if cedula in empleados:
        print("Error: La cédula ya existe en la base de datos.")
        return
    nombres = input("Ingrese nombres = ").strip()
    apellidos = input("Ingrese apellidos = ").strip()
    empleados[cedula] = {"cedula": cedula, "nombres": nombres, "apellidos": apellidos}
    print("Empleado agregado con éxito.")

def consultar_empleado(empleados):
    """Consulta y muestra los datos de un empleado según su cédula."""
    cedula = input("¿Qué cédula desea buscar?: ").strip()
    empleado = empleados.get(cedula)
    if empleado:
        print(f"Cédula = {empleado['cedula']}")
        print(f"Nombres = {empleado['nombres']}")
        print(f"Apellidos = {empleado['apellidos']}")
    else:
        print("El empleado no se encuentra en la base de datos.")

def modificar_empleado(empleados):
    """Modifica los datos de un empleado según su cédula."""
    cedula = input("¿Cuál es la cédula del empleado que desea MODIFICAR?: ").strip()
    if cedula in empleados:
        empleado = empleados[cedula]
        print("Deje en blanco si no desea modificar el campo.")
        nueva_cedula = input(f"Ingrese nueva cédula [{empleado['cedula']}] = ").strip()
        nuevos_nombres = input(f"Ingrese nuevos nombres [{empleado['nombres']}] = ").strip()
        nuevos_apellidos = input(f"Ingrese nuevos apellidos [{empleado['apellidos']}] = ").strip()
        
        if nueva_cedula and nueva_cedula != cedula:
            if nueva_cedula in empleados:
                print("Error: La nueva cédula ya existe en la base de datos.")
                return
            del empleados[cedula]
            cedula = nueva_cedula
        
        empleados[cedula] = {
            "cedula": cedula,
            "nombres": nuevos_nombres or empleado['nombres'],
            "apellidos": nuevos_apellidos or empleado['apellidos']
        }
        print("Empleado modificado con éxito.")
    else:
        print("El empleado no se encuentra en la base de datos.")

def eliminar_empleado(empleados):
    """Elimina un empleado del diccionario según su cédula."""
    cedula = input("¿Cuál es la cédula del empleado que desea ELIMINAR?: ").strip()
    if cedula in empleados:
        del empleados[cedula]
        print("Empleado eliminado con éxito.")
    else:
        print("El empleado no se encuentra en la base de datos.")

def visualizar_base_datos(empleados):
    """Muestra todos los empleados en la base de datos."""
    if not empleados:
        print("La base de datos está vacía.")
    else:
        print("\nBase de datos de empleados:")
        print("-" * 40)
        for empleado in empleados.values():
            print(f"Cédula: {empleado['cedula']}")
            print(f"Nombres: {empleado['nombres']}")
            print(f"Apellidos: {empleado['apellidos']}")
            print("-" * 40)

def menu_principal():
    """Muestra el menú principal y ejecuta las opciones seleccionadas."""
    empleados = cargar_empleados()
    while True:
        print("\nMENÚ")
        print("1. Agregar empleado")
        print("2. Consultar empleado")
        print("3. Modificar datos de empleado")
        print("4. Eliminar empleado")
        print("5. Visualizar base de datos")
        print("6. Guardar y Salir")
        
        opcion = input("\n¿Qué desea hacer? (Elegir entre opciones 1-6): ").strip()
        
        if opcion == "1":
            agregar_empleado(empleados)
        elif opcion == "2":
            consultar_empleado(empleados)
        elif opcion == "3":
            modificar_empleado(empleados)
        elif opcion == "4":
            eliminar_empleado(empleados)
        elif opcion == "5":
            visualizar_base_datos(empleados)
        elif opcion == "6":
            guardar_empleados(empleados)
            print("Datos guardados. Hasta pronto.")
            sys.exit(0)
        else:
            print("\nHas elegido una opción no válida.")

if __name__ == "__main__":
    print("Bienvenido\n")
    menu_principal()