#!/usr/bin/python
'''
    Equipo: Mustafar
    Fecha: 10 de abril de 2020

    Integrantes:
        Félix López Juan Pablo
        López Velásquez Octavio
        Serna Navarro Ángel Emilio

        Server SDK baraja
        Programa: Servidor.
'''

import argparse
from xmlrpc.server import SimpleXMLRPCServer
import logging
import random
import tarjetas
import pickle
import copy


def crear_servidor(ip, puerto):
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    server = SimpleXMLRPCServer((ip, puerto), logRequests=True,)
    return server


def guardar_pickle(baraja, mano):
    '''
        guarda una lista de cartas y un objeto baraja en el servidor
        recibe: un objeto baraja, uso: "baraja"
        recibe: numero de mano (int) uso: mano
        guarda en un archivo .pkl la lista
    '''
    try:
        lista = [baraja, mano]
        nombre_archivo = "pickle.pkl"
        pickle.dump(lista, open(nombre_archivo, "wb"))
        print("Notificación: '" + str(nombre_archivo) + "'" + " se ha actualizado.\n")
    except:
        print("Hubo un problema al guardar el archivo.")


def leer_pkl():
    '''
        Lee un archivo .pkl y devuelve una lista de objetos
        regresa: lista[0] = baraja
                 lista[1] = mano (tamaño de mano)
    '''
    try:
        lista = pickle.load(open("pickle.pkl", "rb"))
    except:
        print("No se pudo leer el archivo solicitado. \n"
              "Intenta hacer una reinserción del mismo.")
    return lista


def existe_jugador(nombre_jugador):
    '''
        Regresa un boolean si existe un jugador
        recibe: nombre del jugador, uso: "Emilio"
    '''
    baraja = leer_pkl()[0]

    if len(baraja.lista_jugadores) > 0:
        for jugador in baraja.lista_jugadores:
            if jugador.nombre == nombre_jugador:
                return True

    return False


def genera_mano(nombre_jugador):
    '''
        Guarda el jugador en baraja, y genera una mano para el mismo
        recibe: un nombre de jugador, uso: "emilio"
        regresa: una lista de cartas
    '''
    if dar_mano():  # se verifica si es posible dar cartas aún
        lista = leer_pkl()  # Se utiliza un pickle para poder usar la información del servidor
        baraja = lista[0]   # objeto baraja que alberga jugadores y cartas
        mano = lista[1]     # tamaño de mano

        if existe_jugador(nombre_jugador) == False:
            # Guarda un jugador en baraja
            tarjetas.genera_jugador(nombre_jugador, baraja)
            # la lista de cartas del jugador
            baraja.genera_mano(mano, nombre_jugador)

        else:  # esto significa que ya debe tener una mano
            # Cambiamos su mano por otra
            cambiar_mano(mano, nombre_jugador)

        print("== Actualización del servidor ==")
        print("\n" + str(nombre_jugador) + ": ha solicitado una mano.")
        print("Quedan:", str(len(baraja.lista_cartas)), "cartas." + " (" + str(len(baraja.lista_cartas)) +"/"+ "52).")
        guardar_pickle(baraja, mano)  # Se guardan los valores sobreescritos
        print("== Actualización exitosa ==\n")
        return obten_mano(nombre_jugador)
    else:
        return 0

def cambiar_mano(mano, nombre_jugador):
    baraja = leer_pkl()[0]
    nueva_mano = baraja.cambia_mano(mano, nombre_jugador)
    guardar_pickle(baraja, mano)
    return nueva_mano


def obten_mano(nombre_jugador):
    '''
        obtiene la mano de un jugador a partir de su nombre
        recibe: nombre_jugador, uso: "Emilio"
        regresa: lista de objetos carta
    '''
    baraja = leer_pkl()[0]

    for j in baraja.lista_jugadores:
        if j.nombre == nombre_jugador:
            jugador = j
            lista_cartas = jugador.despliega_mano(baraja)
            return lista_cartas


def obten_mano_todos():
    '''
        obtiene la mano de todos los jugadores
    '''
    baraja = leer_pkl()[0]

    lista_nombres_jugadores = mostrar_jugadores()
    lista_cartas_jugadores = list()

    for jugador in baraja.lista_jugadores:
        lista_cartas_jugadores.append(jugador.despliega_mano(baraja))

    return lista_nombres_jugadores, lista_cartas_jugadores


def mostrar_jugadores():
    '''
        regresa una lista con los nombres de los jugadores de un objeto baraja
        regresa: lista_nombres
    '''
    lista_jugadores = leer_pkl()[0].lista_jugadores  # baraja.lista_jugadores
    if len(lista_jugadores) > 0:
        lista_nombres = []
        for jugador in lista_jugadores:
            lista_nombres.append(jugador.nombre)
        return lista_nombres
    else:
        return []


def dar_mano():
    '''
        Regresa un boolean dependiendo si es posible o no dar más cartas
    '''
    baraja = leer_pkl()[0]
    mano = leer_pkl()[1]

    if len(baraja.lista_cartas) >= mano:
        return True
    else:
        return False


def obten_puntaje():
    '''
        Calcula la puntuación de todos los jugadores
        Regresa un diccionario de jugador, y un set de empatados
        dicc[jugador] = [pares, tercias]
    '''
    baraja = leer_pkl()[0]
    mano = leer_pkl()[1]

    dicc_puntos = baraja.calcula_puntaje() # key nombre_jugador, value lista[pares, tercias, puntuacion]

    guardar_pickle(baraja, mano)

    return dicc_puntos, definir_ganador(dicc_puntos)

def definir_ganador(dicc_puntos):
    # jugador_pasado = {pares, tercias, puntuacion}
    # jugador_actual = {pares, tercias, puntuacion}
    primera_vez = True
    set_empatados = set()

    for nombre_jugador, jugador_actual in dicc_puntos.items():

        if primera_vez == True:
            nombre_pasado = copy.copy(nombre_jugador)
            jugador_pasado = copy.copy(jugador_actual)
            primera_vez = False
        else:
            pares_pasado = jugador_pasado[0]
            tercias_pasado = jugador_pasado[1]
            puntuacion_pasado = jugador_pasado[2]

            nombre_actual = nombre_jugador
            pares_actual = jugador_actual[0]
            tercias_actual = jugador_actual[1]
            puntuacion_actual = jugador_actual[2]

            if tercias_pasado > 0 and tercias_actual == 0:
                # gana el pasado
                print("Ganó el pasado: 210")
                print(nombre_pasado)
                pass
            elif tercias_pasado == 0 and tercias_actual == 0:
                # no tienen tercias, posiblemente pares
                if pares_pasado > 0 and pares_actual == 0:
                    # gana el pasado
                    print("Ganó el pasado: 216")
                    print(nombre_pasado)
                    pass
                elif pares_pasado == pares_actual:
                    if pares_pasado == 0 and pares_actual == 0:
                        # empate
                        print("Empate: 221")
                        set_empatados = empate(set_empatados, nombre_pasado, nombre_actual, puntuacion_pasado, puntuacion_actual)
                        print("Empate: 223")
                    else:
                        # desempate de puntos
                        if puntuacion_pasado > puntuacion_actual:
                            # gana pasado
                            print("Ganó el pasado: 228")
                            print(nombre_pasado)
                        elif puntuacion_pasado == puntuacion_actual:
                            # empate
                            print("Empate: 232")
                            set_empatados = empate(set_empatados, nombre_pasado, nombre_actual, puntuacion_pasado, puntuacion_actual)
                            print("Empate: 234")
                        else:
                            # gana el actual
                            print("Ganó el actual: 237")
                            print(nombre_actual)
                            nombre_pasado = copy.copy(nombre_jugador)
                            jugador_pasado = copy.copy(jugador_actual)
                else:
                    # gana el actual
                    print("Ganó el actual: 242")
                    print(nombre_actual)
                    nombre_pasado = copy.copy(nombre_jugador)
                    jugador_pasado = copy.copy(jugador_actual)
            elif tercias_pasado == tercias_actual:
                # desempate de puntos
                if puntuacion_pasado > puntuacion_actual:
                    # gana pasado
                    print("Ganó el pasado: 249")
                    print(nombre_pasado)
                elif puntuacion_pasado == puntuacion_actual:
                    # empate
                    print("Empate: 253")
                    set_empatados = empate(set_empatados, nombre_pasado, nombre_actual, puntuacion_pasado, puntuacion_actual)
                    print("Empate: 255")
                else:
                    # gana actual
                    print("Ganó el actual: 258")
                    print(nombre_actual)
                    nombre_pasado = copy.copy(nombre_jugador)
                    jugador_pasado = copy.copy(jugador_actual)
            else:
                # gana el actual
                print("Ganó el pasado: 263")
                print(nombre_actual)
                nombre_pasado = copy.copy(nombre_jugador)
                jugador_pasado = copy.copy(jugador_actual)

            set_empatados = empate(set_empatados, nombre_pasado, nombre_actual, puntuacion_pasado, puntuacion_actual)
            print("268")
            return set_empatados



def empate(set_empatados, nombre_pasado, nombre_actual, puntuacion_pasado, puntuacion_actual):
    '''
        Calcula la forma en que irán yendo los empatados
    '''
    if len(set_empatados) < 1:
        # no hay empatados
        set_empatados.add(nombre_pasado)
        set_empatados.add(nombre_actual)
    else:
        if puntuacion_pasado > puntuacion_actual:
            # los empatados tienen más puntos
            pass
        elif puntuacion_pasado == puntuacion_actual:
            # los empatados tienen los mismos puntos
            set_empatados.add(nombre_actual)
        else:
            # el actual tiene más puntos que los empatados pasados
            set_empatados.clear()
            set_empatados.add(nombre_actual)

    return set_empatados


def numero_rondas(temp):
    temp += 1
    return temp

def salir(nombre_jugador):
    baraja = leer_pkl()[0]
    mano = leer_pkl()[1]  # tamaño de mano
    # se retorna las cartas a la baraja
    baraja.regresa_mano(mano, nombre_jugador)

    print("== Actualización del servidor ==")
    print("\nEl jugador(a):", nombre_jugador, "se ha desconectado.")
    print("Quedan:", (len(baraja.lista_cartas)), "cartas.", "(" + str(len(baraja.lista_cartas)) +"/"+ "52).")
    guardar_pickle(baraja, mano)
    print("== Actualización exitosa ==\n")
    


def prueba_conexion(jugador):
    '''
        SOLO USAR PARA TESTING
    '''
    print("Se conectó", jugador + "s")
    return "Descifraste el mensaje secreto"


def main(ip, puerto, mano):  # dirección IP, puerto, cantidad de cartas por mano
    server = crear_servidor(ip, puerto)

    baraja = tarjetas.Baraja()
    guardar_pickle(baraja, mano)

    server.register_function(prueba_conexion)
    server.register_function(genera_mano)
    server.register_function(mostrar_jugadores)
    server.register_function(obten_mano)
    server.register_function(obten_mano_todos)
    server.register_function(salir)
    server.register_function(cambiar_mano)
    server.register_function(obten_puntaje)
    server.register_function(numero_rondas)
    # Iniciando servidor
    print("\nIniciando servidor...\n")
    try:
        print("===========================\n")
        print("Información del servidor: ")
        print("- Servidor iniciado")
        print("- Dirección IP:", ip)
        print("- Puerto:", puerto)
        print("- Tamaño de mano:", mano)
        print("\n===========================")
        print("\nUsa Control-C para salir.\n")
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nApagando servidor " + "('" + str(direccion) + "', '" +  str(puerto) + "')...\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--direccion', dest='direccion',
                        help="Dirección IP", required=False, default="localhost")
    parser.add_argument('-p', '--puerto', dest='puerto',
                        help="Puerto", type=int, required=False, default=9000)
    parser.add_argument('-m', '--mano', dest='mano',
                        help="Tamaño de mano", type=int, required=False, default=5)
    args = parser.parse_args()
    direccion = args.direccion
    puerto = args.puerto
    mano = args.mano

    main(direccion, puerto, mano)
