class Carrito:
    def __init__(self, cant_prod=0, total_pagar=0):
        """
        Inicializa el carrito con un diccionario de productos vacío,
        la cantidad de productos y el total a pagar.
        """
        self.productos = {}
        self.cant_prod = cant_prod
        self.total_pagar_valor = total_pagar

    def existencia_producto(self, sku):
        """
        Verifica si un producto con el SKU dado está en el carrito.

        Args:
            sku (str): Código de identificación del producto.

        Returns:
            str: Mensaje indicando si el producto está o no en el carrito.
        """
        if sku in self.productos:
            return f"El producto de SKU {sku} sí se encuentra en el carrito."
        else:
            return f"El producto de SKU {sku} no se encuentra en el carrito."

    def agregar_producto(self, sku, cantidad_prod, precio):
        """
        Agrega un producto al carrito o actualiza su cantidad y precio si ya existe.

        Args:
            sku (str): Código de identificación del producto.
            cantidad_prod (int): Cantidad de productos a agregar.
            precio (float): Precio del producto.
        """
        self.productos[sku] = {'cantidad': cantidad_prod, "precio": precio}
        self.total_pagar_valor += cantidad_prod * precio

    def eliminar_producto(self, sku, cantidad_prod):
        """
        Elimina una cantidad específica de un producto del carrito. Si la cantidad
        eliminada es mayor o igual a la cantidad en el carrito, el producto se elimina
        por completo.

        Args:
            sku (str): Código de identificación del producto.
            cantidad_prod (int): Cantidad de productos a eliminar.
        """
        if sku in self.productos:
            producto = self.productos[sku]
            if cantidad_prod >= producto["cantidad"]:
                self.total_pagar_valor -= producto["cantidad"] * producto["precio"]
                del self.productos[sku]
            else:
                producto["cantidad"] -= cantidad_prod
                self.total_pagar_valor -= cantidad_prod * producto["precio"]

    def total_pagar(self):
        """
        Devuelve el total a pagar por los productos en el carrito.

        Returns:
            float: Total a pagar.
        """
        return self.total_pagar_valor

    def consultar_cantidad(self, sku):
        """
        Consulta la cantidad de un producto en el carrito.

        Args:
            sku (str): Código de identificación del producto.

        Returns:
            int: Cantidad del producto en el carrito. Si no está, devuelve 0.
        """
        if sku in self.productos:
            return self.productos[sku]['cantidad']
        return 0

    def validar_presupuesto(self, presupuesto, total_pagar):
        """
        Valida si el presupuesto es suficiente para pagar el total del carrito.

        Args:
            presupuesto (float): Presupuesto disponible.
            total_pagar (float): Total a pagar por los productos en el carrito.
        """
        if presupuesto < total_pagar:
            print("Error: No tienes dinero suficiente")
        else:
            print(f"""Si tienes dinero suficiente.
            {presupuesto} -
            {total_pagar}
            --------------
            {presupuesto - total_pagar}

            Te sobraron {presupuesto - total_pagar}$.    
        """)

#Test carrito

# Crear una instancia del carrito
carrito = Carrito()

# Prueba 1: Agregar productos al carrito
carrito.agregar_producto("123ABC", 2, 100)
print("Prueba 1 - Agregar productos:")
print("Cantidad de 123ABC:", carrito.consultar_cantidad("123ABC"))  # Esperado: 2
print("Total a pagar:", carrito.total_pagar())  # Esperado: 200
print()

# Prueba 2: Eliminar parte de un producto
carrito.eliminar_producto("123ABC", 1)
print("Prueba 2 - Eliminar parte de un producto:")
print("Cantidad de 123ABC:", carrito.consultar_cantidad("123ABC"))  # Esperado: 1
print("Total a pagar:", carrito.total_pagar())  # Esperado: 100
print()

# Prueba 3: Eliminar un producto completamente
carrito.eliminar_producto("123ABC", 1)
print("Prueba 3 - Eliminar un producto completamente:")
print("Cantidad de 123ABC:", carrito.consultar_cantidad("123ABC"))  # Esperado: 0
print("Total a pagar:", carrito.total_pagar())  # Esperado: 0
print()

# Prueba 4: Verificar la existencia de un producto
carrito.agregar_producto("XYZ789", 1, 50)
print("Prueba 4 - Verificar existencia de un producto:")
print(carrito.existencia_producto("XYZ789"))  # Esperado: "El producto de SKU XYZ789 sí se encuentra en el carrito."
print(carrito.existencia_producto("ZZZ999"))  # Esperado: "El producto de SKU ZZZ999 no se encuentra en el carrito."
print()

# Prueba 5: Validar presupuesto
presupuesto = 200
print("Prueba 5 - Validar presupuesto:")
carrito.validar_presupuesto(presupuesto, carrito.total_pagar())  # Dependiendo del total, verificará si el presupuesto es suficiente
print()
