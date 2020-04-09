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
        pickle.dump(lista, open("pickle.pkl", "wb"))
        print("Se actualizó", "pickle.pkl\n")
    except:
        print("Hubo un problema al guardar el archivo")


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
            baraja.cambia_mano(mano, nombre_jugador)

        print(nombre_jugador, "solicitó pedir mano")
        print("Quedan", len(baraja.lista_cartas), "cartas")
        guardar_pickle(baraja, mano)  # Se guardan los valores sobreescritos
        return obten_mano(nombre_jugador)
    else:
        return 0


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


def salir(nombre_jugador):
    baraja = leer_pkl()[0]
    mano = leer_pkl()[1]  # tamaño de mano
    # se retorna las cartas a la baraja
    baraja.regresa_mano(mano, nombre_jugador)

    print("El jugador(a):", nombre_jugador, "se ha desconectadx")
    print("Quedan", len(baraja.lista_cartas), "cartas")
    guardar_pickle(baraja, mano)


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
        print("\nApagando servidor...\n")


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
