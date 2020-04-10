import random
import copy

'''
    Programa del juego de la baraja francesa
'''


class Jugador:
    nombre = None
    mano = None
    puntuacion = None
    ganadas_jeje = None
    def __init__(self, nombre, baraja):
        self.nombre = nombre
        self.mano = []
        self.puntuacion = 0
        self.ganadas_jeje = 0
        baraja.guarda_jugador(self)

    def despliega_mano(self, baraja):
        '''
            imprime la mano de un jugador
            recibe: un objeto baraja
        '''
        cartas_mano = []
        #print("\nJugador: " + self.nombre)
        # print("--------------------\n")
        for carta in self.mano:
            cartas = f"{carta.display(baraja.diccionario_cartas)}"
            # print(cartas)
            cartas_mano.append(cartas)
            # Aquí había una línea de puntuación

        return cartas_mano

    def ordena_mano(self):
        self.mano.sort(key=lambda x: x.valor, reverse=True)


class Carta:
    valor = None
    figura = None

    def __init__(self, valor, figura):
        self.valor = valor
        self.figura = figura

    def __str__(self):
        return f"{self.valor}-{self.figura}"

    def display(self, dict_cartas):
        '''
            POSIBLEMENTE QUEDE EN DESHUSO
        '''
        carta_cara = dict_cartas[self.valor]
        return f"{carta_cara}-{self.figura}"


class Baraja:
    diccionario_cartas = None
    figuras = None
    lista_cartas = None
    lista_jugadores = None

    def __init__(self):
        # El método Genera_lista_cartas() debe de hacer la lista de 52 cartas
        self.diccionario_cartas = {
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "J",
            12: "Q",
            13: "K",
            20: "A",
        }
        # Corazones, Picas, Trébol, Diamante
        self.figuras = ["C", "P", "T", "D"]
        self.lista_cartas = genera_lista_cartas()
        self.lista_jugadores = []

    def genera_mano(self, num_cartas, nombre_jugador):
        '''
            Se genera una nueva lista de cartas revueltas con la cantidad de la mano
            recibe: numero de cartas en mano (int)
            recibe: nombre de jugador (str), uso: "Emilio"
            regresa: una lista de cartas del jugador (list<str>)
        '''
        # debe asignar una mano aleatoriamente a cada uno de los jugadores de la lista

        # busca en la lista el jugador
        for j in self.lista_jugadores:
            if j.nombre == nombre_jugador:
                jugador = j

                jugador.mano = random.sample(self.lista_cartas, num_cartas)

        # Se eliminan las cartas del jugador en la lista de cartas disponibles
                for carta in jugador.mano:
                    self.lista_cartas.remove(carta)

        # ACÁ DEBE HABER UNA FORMA DE REGRESAR LAS CARTAS QUE YA USASTE

                return jugador.mano

    def cambia_mano(self, num_cartas, nombre_jugador):
        '''
            Regresa una mano nueva
            recibe: numero de cartas en mano (int), uso: 5
            recibe: nombre de jugador (str), uso: "Emilio"
            regresa: una lista de cartas del jugador (list<str>)
        '''
        for jugador in self.lista_jugadores:
            if jugador.nombre == nombre_jugador:
                for carta in jugador.mano:
                    # se regresan las cartas a la baraja
                    self.lista_cartas.append(carta)

                jugador.mano.clear()
                jugador.mano = random.sample(
                    self.lista_cartas, num_cartas)  # revolvemos baraja

                for carta in jugador.mano:
                    self.lista_cartas.remove(carta)  # se las damos al jugador

                return jugador.despliega_mano(self)

    def regresa_mano(self, num_cartas, nombre_jugador):
        '''
            Elimina al jugador y regresa su mano
            recibe: numero de cartas en mano (int), uso: 5
            recibe: nombre de jugador (str), uso: "Emilio"
            Regresa un boolean si el jugador ya tenía cartas
        '''
        for jugador in self.lista_jugadores:
            if jugador.nombre == nombre_jugador:
                for carta in jugador.mano:
                    # se regresan las cartas a la baraja
                    self.lista_cartas.append(carta)

                self.lista_jugadores.remove(jugador)

    def guarda_jugador(self, jugador):
        self.lista_jugadores.append(jugador)

    def calcula_puntaje(self):
        '''
            Calcula el puntaje de todos los jugadores
            regresa: diccionario de jugadores con lista de pares y tercias
            dicc[jugador.nombre] = pares:2, tercias:1
            key = jugador.nombre, value = [2, 1]
        '''
        lista_nueva = list()
        dicc_jugadores = dict()

        for jugador in self.lista_jugadores:
            jugador.ordena_mano()

            # Convertimos la mano en una lista nueva de solo números.
            for carta in jugador.mano:
                lista_nueva.append(carta.valor)

            # Contamos el número de cartas repetidas y se guardan en un diccionario
            dicc = {i:lista_nueva.count(i) for i in lista_nueva} #Muchas gracias al Octavio no? que me paso esta cosa un saludaxo
            pares = 0
            tercias = 0

            for valor_carta, repetidos in dicc.items():
                if repetidos == 2: # Es par.
                    pares += 1
                    jugador.puntuacion += valor_carta*repetidos

                elif repetidos == 4: # Son dos pares.
                    pares += 2
                    jugador.puntuacion += valor_carta*repetidos

                elif repetidos == 3: # Es tercia.
                    tercias += 1
                    jugador.puntuacion += valor_carta*repetidos

            dicc_jugadores[jugador.nombre] = [pares, tercias, jugador.puntuacion]

        return dicc_jugadores


def genera_lista_cartas():
    ''' 
        genera una lista de todas las cartas de la baraja (52 cartas)
        y regresa una lista de estas
    '''
    lista_cartas = list()
    for i in range(0, 4):
        if i == 0:
            figura = "♥"  # Corazones
        elif i == 1:
            figura = "♠"  # Picas
        elif i == 2:
            figura = "♣"  # Trébol
        elif i == 3:
            figura = "♦"  # Diamante
        for valor in range(2, 15):  # los valores de las cartas empiezan en 2
            if valor == 14:
                valor = 20  # As vale 20
            carta_nueva = Carta(valor, figura)
            lista_cartas.append(carta_nueva)

    return lista_cartas


def genera_jugador(jugador, baraja):
    '''
        genera los jugadores dentro del objeto baraja
        recibe: un nombre de jugador (string)
        recibe: un objeto baraja
    '''
    nombre = Jugador(jugador, baraja)
