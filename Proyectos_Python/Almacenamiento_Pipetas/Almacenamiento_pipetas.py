# Sistema para almacenamiento de mediciones en laboratorio de metrología.

# Base de datos con todas las pipetas añadidas.
base_de_datos = []

# Cantidad de pipetas añadidas a la base de datos.
pipetas_totales = 0

# Cantidad de pipetas por marca en la base de datos.
p_brand = 0
p_3M = 0
p_rainin = 0
p_pipeteline = 0

def obtener_medida(prompt, min_val, max_val):
    """Solicita una medida numérica y valida que esté en el rango aceptable."""
    while True:
        try:
            medida = float(input(prompt))
            if min_val <= medida <= max_val:
                return medida
            else:
                print(f"¡ALERTA! La medición está fuera del rango aceptable ({min_val}-{max_val}).")
        except ValueError:
            print("¡ERROR! Debe ingresar un número válido.")

def obtener_marca():
    """Solicita y valida la marca de la pipeta."""
    marcas_validas = ["Brand", "3M", "Rainin", "PipeteLine"]
    while True:
        marca = input("\nMarcas:\n -Brand\n -3M\n -Rainin\n -PipeteLine\n\nMarca de la pipeta: ").strip()
        if marca in marcas_validas:
            return marca
        else:
            print("¡ERROR! Marca no válida. Por favor, seleccione una de las opciones disponibles.")

def visualizar_seriales():
    """Muestra todos los seriales con su respectiva marca."""
    if not base_de_datos:
        print("No hay pipetas en la base de datos.")
    else:
        print("\nListado de seriales y marcas:")
        for pipeta in base_de_datos:
            print(f"Serial: {pipeta[1]}, Marca: {pipeta[0]}")

def serial_existe(serial):
    """Verifica si un serial ya existe en la base de datos."""
    return any(pipeta[1] == serial for pipeta in base_de_datos)

for _ in range(100000000):
    menu = input("\n1. Ingresar información de una pipeta.\n2. Consultar información de una pipeta.\n3. Estadísticos.\n4. Visualizar seriales.\n5. Salir.\n\n"
                 "¿Qué desea hacer? (Elegir entre opciones 1, 2, 3, 4 y 5): ").strip()

    if menu == "1":
        pipeta = []  # Información de la pipeta que se desea añadir.

        marca = obtener_marca()
        pipeta.append(marca)
        
        # Actualizar contador de pipetas por marca.
        if marca == "Brand":
            p_brand += 1
        elif marca == "3M":
            p_3M += 1
        elif marca == "Rainin":
            p_rainin += 1
        elif marca == "PipeteLine":
            p_pipeteline += 1
        
        while True:
            serial = input("Inserte el serial de la pipeta: ").strip()
            if serial_existe(serial):
                print("¡ERROR! El serial ya existe en la base de datos. Ingrese un serial único.")
            else:
                pipeta.append(serial)
                break
        
        # Medidas del 10% del volumen nominal.
        medidas1 = []
        v_11 = obtener_medida("Inserte medida del 10% del volumen nominal. #1: ", 90, 110)
        medidas1.append(v_11)
        v_12 = obtener_medida("Inserte medida del 10% del volumen nominal. #2: ", 90, 110)
        medidas1.append(v_12)
        v_13 = obtener_medida("Inserte medida del 10% del volumen nominal. #3: ", 90, 110)
        medidas1.append(v_13)
        media1 = (v_11 + v_12 + v_13) / 3
        medidas1.append(media1)
        pipeta.append(medidas1)
        
        # Medidas del 100% del volumen nominal.
        medidas2 = []
        v_21 = obtener_medida("Inserte medida del 100% del volumen nominal. #1: ", 900, 1100)
        medidas2.append(v_21)
        v_22 = obtener_medida("Inserte medida del 100% del volumen nominal. #2: ", 900, 1100)
        medidas2.append(v_22)
        v_23 = obtener_medida("Inserte medida del 100% del volumen nominal. #3: ", 900, 1100)
        medidas2.append(v_23)
        media2 = (v_21 + v_22 + v_23) / 3
        medidas2.append(media2)
        pipeta.append(medidas2)

        pipetas_totales += 1
        base_de_datos.append(pipeta)

    elif menu == "2":
        buscar_pipeta = input("Inserte el número de serial que desea consultar: ").strip()
        disponibilidad = False
        
        for pipeta in base_de_datos:
            if buscar_pipeta == pipeta[1]:
                disponibilidad = True
                print(f'''
                Marca: {pipeta[0]}
                Serial: {pipeta[1]}
                Medida 1. #1: {pipeta[2][0]}
                Medida 1. #2: {pipeta[2][1]}
                Medida 1. #3: {pipeta[2][2]}
                Media de medida 1: {pipeta[2][3]}
                Medida 2. #1: {pipeta[3][0]}
                Medida 2. #2: {pipeta[3][1]}
                Medida 2. #3: {pipeta[3][2]}
                Media de medida 2: {pipeta[3][3]}''')
                break
        
        if not disponibilidad:
            print(f"La pipeta con serial -{buscar_pipeta}- no se encuentra en la base de datos.")

    elif menu == "3":
        print(f"\nPipetas ingresadas:\n\nBrand: {p_brand} pipeta/s.\n3M: {p_3M} pipeta/s.\nRainin: {p_rainin} pipeta/s.\nPipeteLine: {p_pipeteline} pipeta/s.\n")

    elif menu == "4":
        visualizar_seriales()

    elif menu == "5":
        break

    else:
        print("\nERROR\nSe ha ingresado una opción no válida.\nIntente de nuevo.")
