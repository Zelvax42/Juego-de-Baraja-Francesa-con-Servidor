import random


class Jugador:
    nombre = None
    mano = None
    puntuacion = None

    def __init__(self, nombre, baraja):
        self.nombre = nombre
        self.mano = []
        self.puntuacion = 0
        baraja.guarda_jugador(self)

    def despliega_mano(self, baraja):
        '''
            imprime la mano de un jugador
            recibe: un objeto baraja
        '''
        cartas_mano = []
        print("\nJugador: " + self.nombre)
        print("--------------------\n")
        for carta in self.mano:
            cartas = f"{carta.display(baraja.diccionario_cartas)}"
            print(cartas)
            cartas_mano.append(cartas)
            #Aquí había una línea de puntuación

        returns = cartas_mano
        return returns

class Carta:
    valor = None
    figura = None

    def __init__(self, valor, figura):
        self.valor = valor
        self.figura = figura

    def __str__(self):
        '''
            POSIBLEMENTE QUEDE EN DESHUSO
        '''
        return f"{self.valor}-{self.figura}"

    def display(self, dict_cartas):
        carta_cara = dict_cartas[self.valor]
        return f"{carta_cara}-{self.figura}"


class Baraja:
    diccionario_cartas = None
    figuras = None
    lista_cartas = None
    lista_jugadores = None

    def __init__(self, lista_cartas):
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
        self.lista_cartas = lista_cartas
        self.lista_jugadores = []

    def genera_mano(self, num_cartas):
        '''
            Se genera una nueva lista de cartas revueltas con la cantidad de la mano
        '''
        # debe asignar una mano aleatoriamente a cada uno de los jugadores de la lista

        for jugador in self.lista_jugadores:
            jugador.mano = random.sample(self.lista_cartas, num_cartas)

            for carta in jugador.mano:  # Se elimina las cartas usadas por el jugador en la lista vieja
                self.lista_cartas.remove(carta)

    def guarda_jugador(self, jugador):
        self.lista_jugadores.append(jugador)
