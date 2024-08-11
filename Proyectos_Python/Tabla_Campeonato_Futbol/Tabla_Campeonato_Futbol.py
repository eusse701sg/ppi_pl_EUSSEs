class Equipo:
    """Clase para representar un equipo en la liga de fútbol."""

    def __init__(self, nombre, puntos=0, partidos_jugados=0, partidos_ganados=0, partidos_perdidos=0, partidos_empats=0, goles_favor=0, goles_contra=0, diferencia_goles=0):
        """
        Inicializa un equipo con sus estadísticas básicas.

        Args:
            nombre (str): Nombre del equipo.
            puntos (int, opcional): Puntos acumulados. Por defecto es 0.
            partidos_jugados (int, opcional): Partidos jugados. Por defecto es 0.
            partidos_ganados (int, opcional): Partidos ganados. Por defecto es 0.
            partidos_perdidos (int, opcional): Partidos perdidos. Por defecto es 0.
            partidos_empats (int, opcional): Partidos empatados. Por defecto es 0.
            goles_favor (int, opcional): Goles a favor. Por defecto es 0.
            goles_contra (int, opcional): Goles en contra. Por defecto es 0.
            diferencia_goles (int, opcional): Diferencia de goles. Por defecto es 0.
        """
        self.nombre = nombre
        self.puntos = puntos
        self.partidos_jugados = partidos_jugados
        self.partidos_ganados = partidos_ganados
        self.partidos_perdidos = partidos_perdidos
        self.partidos_empats = partidos_empats
        self.goles_favor = goles_favor
        self.goles_contra = goles_contra
        self.diferencia_goles = diferencia_goles

    def actualizar_datos(self, puntos, partidos_jugados, partidos_ganados, partidos_perdidos, partidos_empats, goles_favor, goles_contra, diferencia_goles):
        """
        Actualiza las estadísticas del equipo con nuevos datos.

        Args:
            puntos (int): Puntos a sumar.
            partidos_jugados (int): Partidos jugados a sumar.
            partidos_ganados (int): Partidos ganados a sumar.
            partidos_perdidos (int): Partidos perdidos a sumar.
            partidos_empats (int): Partidos empatados a sumar.
            goles_favor (int): Goles a favor a sumar.
            goles_contra (int): Goles en contra a sumar.
            diferencia_goles (int): Diferencia de goles a sumar.
        """
        self.puntos += puntos
        self.partidos_jugados += partidos_jugados
        self.partidos_ganados += partidos_ganados
        self.partidos_perdidos += partidos_perdidos
        self.partidos_empats += partidos_empats
        self.goles_favor += goles_favor
        self.goles_contra += goles_contra
        self.diferencia_goles += diferencia_goles


class TablaPosiciones:
    """Clase para gestionar la tabla de posiciones de los equipos en la liga."""

    def __init__(self, tamaño=20):
        """
        Inicializa la tabla de posiciones con el tamaño dado.

        Args:
            tamaño (int, opcional): Tamaño de la tabla. Por defecto es 20.
        """
        self.tamaño = tamaño
        self.equipos = [None] * tamaño

    def _hash(self, nombre):
        """
        Calcula el valor hash para un nombre de equipo.

        Args:
            nombre (str): Nombre del equipo.

        Returns:
            int: Valor hash del nombre del equipo.
        """
        valor_hash = 5381
        for caracter in nombre:
            valor_hash = (valor_hash * 33) ^ ord(caracter)
        return valor_hash % self.tamaño

    def agregar_actualizar_equipo(self, nombre_equipo, equipo):
        """
        Agrega un equipo a la tabla o lo actualiza si ya existe.

        Args:
            nombre_equipo (str): Nombre del equipo.
            equipo (Equipo): Instancia de la clase Equipo.
        """
        indice = self._hash(nombre_equipo)
        while self.equipos[indice]:
            if self.equipos[indice][0] == nombre_equipo:
                self.equipos[indice] = [nombre_equipo, equipo]
                return
            indice = (indice + 1) % self.tamaño
        self.equipos[indice] = [nombre_equipo, equipo]

    def eliminar_equipo(self, nombre_equipo):
        """
        Elimina un equipo de la tabla.

        Args:
            nombre_equipo (str): Nombre del equipo a eliminar.

        Returns:
            list: Lista con el nombre y la instancia del equipo eliminado o None si no se encontró.
        """
        indice = self._hash(nombre_equipo)
        while self.equipos[indice]:
            if self.equipos[indice][0] == nombre_equipo:
                eliminado = self.equipos[indice]
                self.equipos[indice] = None
                return eliminado
            indice = (indice + 1) % self.tamaño
        return None

    def obtener_equipo(self, nombre_equipo):
        """
        Obtiene un equipo de la tabla.

        Args:
            nombre_equipo (str): Nombre del equipo a obtener.

        Returns:
            Equipo: Instancia del equipo o None si no se encontró.
        """
        indice = self._hash(nombre_equipo)
        while self.equipos[indice]:
            if self.equipos[indice][0] == nombre_equipo:
                return self.equipos[indice][1]
            indice = (indice + 1) % self.tamaño
        return None

    def ingresar_partido(self, nombre_equipo1, goles_equipo1, nombre_equipo2, goles_equipo2):
        """
        Registra el resultado de un partido entre dos equipos.

        Args:
            nombre_equipo1 (str): Nombre del primer equipo.
            goles_equipo1 (int): Goles del primer equipo.
            nombre_equipo2 (str): Nombre del segundo equipo.
            goles_equipo2 (int): Goles del segundo equipo.

        Returns:
            bool: True si el partido se registró correctamente, False en caso contrario.
        """
        equipo1 = self.obtener_equipo(nombre_equipo1)
        equipo2 = self.obtener_equipo(nombre_equipo2)
        if equipo1 is None:
            print(f"El equipo {nombre_equipo1} no se encuentra en la tabla.")
            return False
        if equipo2 is None:
            print(f"El equipo {nombre_equipo2} no se encuentra en la tabla.")
            return False

        if goles_equipo1 > goles_equipo2:
            equipo1.actualizar_datos(3, 1, 1, 0, 0, goles_equipo1, goles_equipo2, goles_equipo1 - goles_equipo2)
            equipo2.actualizar_datos(0, 1, 0, 1, 0, goles_equipo2, goles_equipo1, goles_equipo2 - goles_equipo1)
        elif goles_equipo1 < goles_equipo2:
            equipo1.actualizar_datos(0, 1, 0, 1, 0, goles_equipo1, goles_equipo2, goles_equipo1 - goles_equipo2)
            equipo2.actualizar_datos(3, 1, 1, 0, 0, goles_equipo2, goles_equipo1, goles_equipo2 - goles_equipo1)
        else:
            equipo1.actualizar_datos(1, 1, 0, 0, 1, goles_equipo1, goles_equipo2, goles_equipo1 - goles_equipo2)
            equipo2.actualizar_datos(1, 1, 0, 0, 1, goles_equipo2, goles_equipo1, goles_equipo2 - goles_equipo1)

        return True

    def imprimir_tabla(self):
        """
        Imprime la tabla de posiciones ordenada por puntos.
        """
        equipos_ordenados = [equipo for equipo in self.equipos if equipo is not None]
        equipos_ordenados.sort(key=lambda x: (x[1].puntos, x[1].diferencia_goles), reverse=True)
        
        print(f"{'Nombre':<20} {'PTS':<5} {'PJ':<5} {'PG':<5} {'PP':<5} {'PE':<5} {'GF':<5} {'GC':<5} {'DG':<5}")
        for equipo in equipos_ordenados:
            print(f"{equipo[1].nombre:<20} {equipo[1].puntos:<5} {equipo[1].partidos_jugados:<5} "
                f"{equipo[1].partidos_ganados:<5} {equipo[1].partidos_perdidos:<5} {equipo[1].partidos_empats:<5} "
                f"{equipo[1].goles_favor:<5} {equipo[1].goles_contra:<5} {equipo[1].diferencia_goles:<5}")


    def mostrar_mejores8(self):
        """
        Muestra los 8 mejores equipos ordenados por puntos y diferencia de goles.
        """
        equipos_ordenados = [equipo for equipo in self.equipos if equipo is not None]
        equipos_ordenados.sort(key=lambda x: (x[1].puntos, x[1].diferencia_goles), reverse=True)
        equipos_ordenados = equipos_ordenados[:8]
        
        print("\nLos mejores 8 equipos son:")
        print(f"{'Nombre':<20} {'PTS':<5} {'PJ':<5} {'PG':<5} {'PP':<5} {'PE':<5} {'GF':<5} {'GC':<5} {'DG':<5}")
        for equipo in equipos_ordenados:
            print(f"{equipo[1].nombre:<20} {equipo[1].puntos:<5} {equipo[1].partidos_jugados:<5} "
                f"{equipo[1].partidos_ganados:<5} {equipo[1].partidos_perdidos:<5} {equipo[1].partidos_empats:<5} "
                f"{equipo[1].goles_favor:<5} {equipo[1].goles_contra:<5} {equipo[1].diferencia_goles:<5}")

    def equipos_con_prom_gol_fav(self):
        """
        Muestra los equipos con una diferencia de goles favorable.

        Returns:
            list: Lista de equipos con diferencia de goles positiva.
        """
        equipos_favorables = [equipo for equipo in self.equipos if equipo is not None and equipo[1].diferencia_goles > 0]
        print("Equipos con promedio de gol favorable:")
        for equipo in equipos_favorables:
            print(equipo[0], equipo[1].diferencia_goles)
        return equipos_favorables

    def promedio_equipo(self, nombre_equipo):
        """
        Calcula el promedio de puntos del equipo dado.

        Args:
            nombre_equipo (str): Nombre del equipo.

        Returns:
            float: Promedio de puntos del equipo.
        """
        equipo = self.obtener_equipo(nombre_equipo)
        if equipo is None:
            print(f"El equipo {nombre_equipo} no se encuentra en la tabla.")
            return None
        puntos_totales = equipo.puntos
        puntos_posibles = equipo.partidos_jugados * 3
        promedio = puntos_totales / puntos_posibles
        print(f"Promedio del equipo {equipo.nombre} es: {promedio:.2f}")
        return promedio

    def peor_equipo(self):
        """
        Muestra el equipo que más ha perdido.

        Returns:
            str: Nombre del equipo que más ha perdido.
        """
        equipos_ordenados = [equipo for equipo in self.equipos if equipo is not None]
        equipos_ordenados.sort(key=lambda x: x[1].partidos_perdidos, reverse=True)
        print(f"El equipo que más ha perdido es: {equipos_ordenados[0][0]}")

    def descendidos(self, numero_descendidos):
        """
        Muestra los equipos que descenderán.

        Args:
            numero_descendidos (int): Número de equipos que descenderán.

        Returns:
            list: Lista de equipos que descenderán.
        """
        equipos_ordenados = [equipo for equipo in self.equipos if equipo is not None]
        equipos_ordenados.sort(key=lambda x: (x[1].puntos, x[1].diferencia_goles, x[1].goles_favor))
        equipos_descendidos = equipos_ordenados[:numero_descendidos]
        print(f"Descenderán {numero_descendidos} equipo/s, estos son:")
        for equipo in equipos_descendidos:
            print(equipo[0])
        return equipos_descendidos

    def porteria_menos_vencida(self):
        """
        Muestra el equipo con la portería menos vencida.

        Returns:
            str: Nombre del equipo con la menor cantidad de goles en contra.
        """
        equipos_ordenados = [equipo for equipo in self.equipos if equipo is not None]
        equipos_ordenados.sort(key=lambda x: x[1].goles_contra)
        print(f"La portería menos vencida es la de: {equipos_ordenados[0][0]}")

    def reiniciar_tabla(self):
        """
        Reinicia las estadísticas de todos los equipos para una nueva temporada.
        """
        for equipo in self.equipos:
            if equipo is not None:
                equipo[1].puntos = 0
                equipo[1].partidos_jugados = 0
                equipo[1].partidos_ganados = 0
                equipo[1].partidos_perdidos = 0
                equipo[1].partidos_empats = 0
                equipo[1].goles_favor = 0
                equipo[1].goles_contra = 0
                equipo[1].diferencia_goles = 0


# Crear equipos
equipo1 = Equipo("Equipo A")
equipo2 = Equipo("Equipo B")
equipo3 = Equipo("Equipo C")
equipo4 = Equipo("Equipo D")
equipo5 = Equipo("Equipo E")
equipo6 = Equipo("Equipo F")
equipo7 = Equipo("Equipo G")
equipo8 = Equipo("Equipo H")
equipo9 = Equipo("Equipo I")
equipo10 = Equipo("Equipo J")

# Crear la tabla de posiciones
tabla = TablaPosiciones(tamaño=10)

# Agregar equipos a la tabla
tabla.agregar_actualizar_equipo("Equipo A", equipo1)
tabla.agregar_actualizar_equipo("Equipo B", equipo2)
tabla.agregar_actualizar_equipo("Equipo C", equipo3)
tabla.agregar_actualizar_equipo("Equipo D", equipo4)
tabla.agregar_actualizar_equipo("Equipo E", equipo5)
tabla.agregar_actualizar_equipo("Equipo F", equipo6)
tabla.agregar_actualizar_equipo("Equipo G", equipo7)
tabla.agregar_actualizar_equipo("Equipo H", equipo8)
tabla.agregar_actualizar_equipo("Equipo I", equipo9)
tabla.agregar_actualizar_equipo("Equipo J", equipo10)

# Registrar partidos
tabla.ingresar_partido("Equipo A", 2, "Equipo B", 1)
tabla.ingresar_partido("Equipo C", 0, "Equipo D", 3)
tabla.ingresar_partido("Equipo E", 1, "Equipo F", 1)
tabla.ingresar_partido("Equipo G", 2, "Equipo H", 2)
tabla.ingresar_partido("Equipo I", 4, "Equipo J", 0)

# Imprimir la tabla de posiciones
print("\nTabla de posiciones:\n")
tabla.imprimir_tabla()

# Mostrar los 8 mejores equipos
print("\n")
tabla.mostrar_mejores8()

# Mostrar equipos con promedio de goles favorable
print("\n")
tabla.equipos_con_prom_gol_fav()

# Calcular y mostrar el promedio de puntos de un equipo
print("\n")
tabla.promedio_equipo("Equipo A")

# Mostrar el equipo que más ha perdido
print("\n")
tabla.peor_equipo()

# Mostrar los equipos que descenderán
print("\n")
tabla.descendidos(3)

# Mostrar el equipo con la portería menos vencida
print("\n")
tabla.porteria_menos_vencida()

# Reiniciar la tabla
print("\nReiniciar tabla y mostrar la tabla después del reinicio:\n")
tabla.reiniciar_tabla()
tabla.imprimir_tabla()
