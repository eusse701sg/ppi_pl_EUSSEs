import json
import os

def cargar_datos():
    """Carga los datos desde un archivo JSON."""
    directorio_actual= os.path.dirname(__file__)
    file_path = os.path.join(directorio_actual, 'datos.json')
    try:
        with open(file_path, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("Archivo de datos no encontrado. Se iniciará con datos vacíos.")
        return {
            "productos": {},
            "producto_totales": 0,
            "ventas_totales": {},
            "ventas_total": 0,
            "sesion": {}
        }
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON. Se iniciará con datos vacíos.")
        return {
            "productos": {},
            "producto_totales": 0,
            "ventas_totales": {},
            "ventas_total": 0,
            "sesion": {}
        }

def guardar_datos(datos):
    """Guarda los datos en un archivo JSON."""
    directorio_actual= os.path.dirname(__file__)
    file_path = os.path.join(directorio_actual, 'datos.json')
    try:
        with open(file_path, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
        print("Datos guardados exitosamente.")
    except IOError:
        print("Error al guardar los datos.")

def autenticar(datos):
    """Solicita y verifica las credenciales del usuario."""
    while True:
        usuario = input("Ingrese su nombre de usuario: ")
        contraseña = input("Ingrese su contraseña (solo números): ")
        if not contraseña.isdigit():
            print("La contraseña solo debe contener números. Intente de nuevo.")
            continue
        if usuario in datos["sesion"] and datos["sesion"][usuario] == int(contraseña):
            print("Autenticación exitosa.")
            return True
        else:
            print("Credenciales incorrectas. Intente de nuevo.")
        if input("¿Desea intentar de nuevo? (s/n): ").lower() != 's':
            return False

def ver_productos(datos):
    """Muestra todos los productos en el inventario."""
    if not datos["productos"]:
        print("No hay productos en el inventario.")
    else:
        print("\n--- Lista de Productos ---")
        for codigo, producto in datos["productos"].items():
            print(f"Código: {codigo}")
            print(f"Nombre: {producto['Nombre']}")
            print(f"Precio: {producto['Precio']}")
            print(f"Inventario: {producto['Inventario']}")
            print("-------------------------")

def agregar_producto(datos):
    """Agrega un nuevo producto al inventario."""
    codigo = input("Ingrese el código del nuevo producto: ")
    if codigo in datos["productos"]:
        print("Este código de producto ya existe.")
        return

    nombre = input("Ingrese el nombre del producto: ")
    while True:
        precio = (input("Ingrese el precio del producto: "))
        if not precio.isdigit():
            print("El precio debe ser un número entero.")
        else:
            precio = int(precio)
            break
    while True:
        inventario = (input("Ingrese la cantidad en inventario: "))
        if not inventario.isdigit():
            print("El inventario debe ser un número entero.")
        else:
            inventario = int(inventario)
            break

    datos["productos"][codigo] = {
        "Nombre": nombre,
        "Precio": precio,
        "Inventario": inventario
    }
    datos["producto_totales"] += 1
    print("Producto agregado con éxito.")
    guardar_datos(datos)

def buscar_producto(datos):
    """Busca y muestra la información de un producto específico."""
    codigo = input("Ingrese el código del producto que desea consultar: ")
    producto = datos["productos"].get(codigo)
    if producto:
        print(f"Código: {codigo}")
        print(f"Nombre: {producto['Nombre']}")
        print(f"Precio: {producto['Precio']}")
        print(f"Inventario: {producto['Inventario']}")
    else:
        print(f"El producto con el código {codigo} no se encuentra en la base de datos.")

def editar_producto(datos):
    """Edita la información de un producto existente."""
    codigo = input("Ingrese el código del producto a modificar: ")
    if codigo in datos["productos"]:
        nombre = input("Ingrese nuevo nombre : ")
        while True:
            precio = input("Ingrese nuevo precio: ")
            if not precio.isdigit():
                print("El precio debe ser un número entero.")
            else:
                precio = int(precio)
                break
        while True:
            inventario = input("Ingrese nuevo inventario: ")
            if not inventario.isdigit():
                print("El inventario debe ser un número entero.")
            else:
                inventario = int(inventario)
                break
        
        if nombre:
            datos["productos"][codigo]["Nombre"] = nombre
        if precio:
            datos["productos"][codigo]["Precio"] = int(precio)
        if inventario:
            datos["productos"][codigo]["Inventario"] = int(inventario)
        
        print("Producto modificado con éxito.")
        guardar_datos(datos)
    else:
        print(f"El producto con el código {codigo} no se encuentra en la base de datos.")

def eliminar_producto(datos):
    """Elimina un producto del inventario."""
    codigo = input("Ingrese el código del producto que desea eliminar: ")
    if codigo in datos["productos"]:
        del datos["productos"][codigo]
        datos["producto_totales"] -= 1
        print("Producto eliminado con éxito.")
        guardar_datos(datos)
    else:
        print(f"El producto con el código {codigo} no se encuentra en la base de datos.")

def ingresar_venta(datos):
    """Registra una nueva venta."""
    codigo_venta = input("Ingrese un código de venta: ")
    fecha_venta = input("Ingrese la fecha: ")
    doc_cliente = input("Ingrese el documento del cliente: ")
    nom_vendedor = input("Ingrese el nombre del vendedor: ")

    productos_comprados = {}
    precios_prod = {}

    while True:
        id_prod = input("Ingrese el código del producto: ")
        if id_prod not in datos["productos"]:
            print("Producto no encontrado.")
            continue

        cant_prod = int(input("Ingrese la cantidad que llevará del producto: "))
        cant_disp = datos["productos"][id_prod]["Inventario"]

        if cant_prod <= cant_disp:
            datos["productos"][id_prod]["Inventario"] -= cant_prod
            productos_comprados[id_prod] = cant_prod
            precios_prod[id_prod] = datos["productos"][id_prod]["Precio"]
        else:
            print(f"No hay suficiente inventario. Solo hay {cant_disp} disponibles.")

        if input("¿Desea agregar otro producto? (s/n): ").lower() != 's':
            break

    venta = {
        "Fecha": fecha_venta,
        "Cliente": doc_cliente,
        "Productos": productos_comprados,
        "Vendedor": nom_vendedor,
        "Precios": precios_prod
    }

    datos["ventas_totales"][codigo_venta] = venta
    datos["ventas_total"] += 1
    guardar_datos(datos)
    print("Venta registrada con éxito.")

def ver_ventas(datos):
    """Muestra todas las ventas realizadas."""
    for id_venta, venta in datos["ventas_totales"].items():
        print(f"Código venta: {id_venta}")
        print(f"Fecha: {venta['Fecha']}")
        total_productos = sum(venta['Productos'].values())
        print(f"Productos totales: {total_productos}")
        total_precio = sum(venta['Precios'][prod] * cant for prod, cant in venta['Productos'].items())
        print(f"Precio total: {total_precio}")
        print()

def buscar_venta(datos):
    """Busca y muestra la información de una venta específica."""
    codigo_venta = input("Ingrese el código de venta que desea consultar: ")
    venta = datos["ventas_totales"].get(codigo_venta)
    if venta:
        print(f"Código venta: {codigo_venta}")
        print(f"Fecha: {venta['Fecha']}")
        print(f"Cliente: {venta['Cliente']}")
        print(f"Vendedor: {venta['Vendedor']}")
        for prod, cant in venta['Productos'].items():
            nombre_prod = datos["productos"][prod]["Nombre"]
            precio_prod = venta['Precios'][prod]
            print(f"Producto: {nombre_prod}, Cantidad: {cant}, Precio: {precio_prod}")
        total_precio = sum(venta['Precios'][prod] * cant for prod, cant in venta['Productos'].items())
        print(f"Precio total: {total_precio}")
    else:
        print(f"La venta con el código {codigo_venta} no se encuentra en la base de datos.")

def editar_venta(datos):
    """Edita la información de una venta existente."""
    codigo_venta = input("Ingrese el código de la venta a modificar: ")
    if codigo_venta in datos["ventas_totales"]:
        nueva_fecha = input("Ingrese la nueva fecha (dejar en blanco para no cambiar): ")
        nuevo_vendedor = input("Ingrese el nuevo nombre del vendedor (dejar en blanco para no cambiar): ")

        if nueva_fecha:
            datos["ventas_totales"][codigo_venta]["Fecha"] = nueva_fecha
        if nuevo_vendedor:
            datos["ventas_totales"][codigo_venta]["Vendedor"] = nuevo_vendedor

        print("Venta modificada con éxito.")
        guardar_datos(datos)
    else:
        print(f"La venta con el código {codigo_venta} no se encuentra en la base de datos.")

def imprimir_factura(datos):
    """Imprime la factura de una venta en un archivo de texto."""
    codigo_venta = input("Ingrese el código de venta que desea imprimir: ")
    venta = datos["ventas_totales"].get(codigo_venta)
    if venta:
        directorio_actual = os.path.dirname(__file__)
        directorio_facturas = os.path.join(directorio_actual, "Facturas")
        if not os.path.exists(directorio_facturas):
            os.makedirs(directorio_facturas)
        factura_path = os.path.join(directorio_facturas, f"factura-#{codigo_venta}.txt")
        with open(factura_path, "w") as archivo:
            archivo.write(f"""
                Tienda S.A.S

        800200100-0
        Teléfono: 589 63 52
        Resolución DIAN 1918165549/8156
        Autorizada el: 2019/01/22 :
        Prefijo POS Del: 1 Al: 100000
        Responsable de IVA
        --------------------------------------------------------
                Factura de Venta
        Código Factura: {codigo_venta}           
        Fecha: {venta['Fecha']}
        Cliente: {venta['Cliente']}
        Vendedor: {venta['Vendedor']}
        """)
            for prod, cant in venta['Productos'].items():
                nombre_prod = datos["productos"][prod]["Nombre"]
                precio_prod = venta['Precios'][prod]
                archivo.write(f"""
        Producto: {nombre_prod}
        Cantidad: {cant}
        Precio unitario: {precio_prod}
        """)
            total_precio = sum(venta['Precios'][prod] * cant for prod, cant in venta['Productos'].items())
            archivo.write(f"\nTotal: {total_precio}")
        print(f"Factura impresa en Facturas/factura-#{codigo_venta}.txt")
    else:
        print(f"La venta con el código {codigo_venta} no se encuentra en la base de datos.")

def menu_estadisticas(datos):
    """Muestra estadísticas de ventas."""
    print(f"1. Número de ventas totales: {datos['ventas_total']}")

    total_ventas = sum(
        sum(venta['Precios'][prod] * cant for prod, cant in venta['Productos'].items())
        for venta in datos["ventas_totales"].values()
    )
    print(f"2. Dinero total vendido: {total_ventas}")

    if datos['ventas_total'] > 0:
        promedio_venta = total_ventas / datos['ventas_total']
        print(f"3. Promedio de dinero de venta: {promedio_venta:.2f}")

        total_productos = sum(
            sum(venta['Productos'].values())
            for venta in datos["ventas_totales"].values()
        )
        promedio_productos = total_productos / datos['ventas_total']
        print(f"4. Promedio de productos por venta: {promedio_productos:.2f}")

    # Producto más vendido
    ventas_por_producto = {}
    for venta in datos["ventas_totales"].values():
        for prod, cant in venta['Productos'].items():
            ventas_por_producto[prod] = ventas_por_producto.get(prod, 0) + cant
    
    if ventas_por_producto:
        max_ventas = max(ventas_por_producto.values())
        productos_mas_vendidos = [prod for prod, ventas in ventas_por_producto.items() if ventas == max_ventas]
        print("5. Producto(s) más vendido(s):")
        for prod in productos_mas_vendidos:
            print(f"   {datos['productos'][prod]['Nombre']} - {max_ventas} unidades")
    else:
        print("No hay ventas registradas.")

def crear_credenciales(datos):
    """Crea nuevas credenciales de acceso."""
    while True:
        nuevo_usuario = input("Inserte el nuevo usuario: ")
        if nuevo_usuario in datos["sesion"]:
            print("Este nombre de usuario ya existe. Por favor, elija otro.")
        else:
            break
    nueva_contraseña = int(input("Inserte la nueva contraseña (solo números): "))
    datos["sesion"][nuevo_usuario] = nueva_contraseña
    print("Credenciales creadas con éxito.")
    guardar_datos(datos)

def ver_credenciales(datos):
    """Muestra las credenciales de acceso actuales."""
    print("Usuario - Contraseña")
    for usuario, contraseña in datos["sesion"].items():
        print(f"{usuario} - {contraseña}")

def eliminar_credenciales(datos):
    """Elimina credenciales de acceso existentes."""
    usuario = input("Ingrese el usuario que desea eliminar: ")
    if usuario in datos["sesion"]:
        del datos["sesion"][usuario]
        print("Credenciales eliminadas con éxito.")
        guardar_datos(datos)
    else:
        print(f"El usuario {usuario} no se encuentra en la base de datos.")

def menu_principal():
    """Muestra el menú principal y maneja la interacción del usuario."""
    datos = cargar_datos()
    datos["sesion"]["admin"] = 1234 #Usuario admin, Contraseña: 1234 por defecto.
    if not autenticar(datos):
        print("Autenticación fallida. El programa se cerrará.")
        return

    while True:
        print("\n--- Menú Principal ---")
        print("1. Ver todos los productos")
        print("2. Agregar nuevo producto")
        print("3. Buscar producto")
        print("4. Editar producto")
        print("5. Eliminar producto")
        print("6. Ingresar venta")
        print("7. Ver ventas")
        print("8. Buscar venta")
        print("9. Editar venta")
        print("10. Imprimir factura")
        print("11. Ver estadísticas")
        print("12. Gestionar credenciales")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            ver_productos(datos)
        elif opcion == "2":
            agregar_producto(datos)
        elif opcion == "3":
            buscar_producto(datos)
        elif opcion == "4":
            editar_producto(datos)
        elif opcion == "5":
            eliminar_producto(datos)
        elif opcion == "6":
            ingresar_venta(datos)
        elif opcion == "7":
            ver_ventas(datos)
        elif opcion == "8":
            buscar_venta(datos)
        elif opcion == "9":
            editar_venta(datos)
        elif opcion == "10":
            imprimir_factura(datos)
        elif opcion == "11":
            menu_estadisticas(datos)
        elif opcion == "12":
            menu_credenciales(datos)
        elif opcion == "0":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

def menu_credenciales(datos):
    """Muestra el menú de gestión de credenciales y maneja la interacción del usuario."""
    while True:
        print("\n--- Menú de Credenciales ---")
        print("1. Crear nuevas credenciales")
        print("2. Ver credenciales")
        print("3. Eliminar credenciales")
        print("0. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            crear_credenciales(datos)
        elif opcion == "2":
            ver_credenciales(datos)
        elif opcion == "3":
            eliminar_credenciales(datos)
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu_principal()