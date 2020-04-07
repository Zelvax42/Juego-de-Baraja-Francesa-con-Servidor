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
        print("Se actualizó", "pickle.pkl")
    except:
        print("Hubo un problema al guardar el archivo")


def leer_pkl():
    '''
        Lee un archivo .pkl y devuelve una lista de objetos
        regresa: lista[0] = baraja
                 lista[1] = mano
    '''
    try:
        lista = pickle.load(open("pickle.pkl", "rb"))
    except:
        print("No se pudo leer el archivo solicitado. \n"
              "Intenta hacer una reinserción del mismo.")
    return lista


def pedir_mano(jugador):
    '''
        Guarda el jugador en baraja, y te asigna una mano
        recibe: un nombre de jugador, uso: "emilio"
        regresa: una lista de cartas
    '''
    lista = leer_pkl() # Se utiliza un pickle para poder usar la información del servidor
    baraja = lista[0]
    mano = lista[1]
    tarjetas.genera_jugador(jugador, baraja)
    lista_cartas = baraja.genera_mano(mano, jugador)
    print(jugador, "Solicitó pedir mano")
    guardar_pickle(baraja, mano) # Se guardan los valores sobreescritos
    return lista_cartas


def prueba_conexion(jugador):
    '''
        SOLO USAR PARA TESTING
    '''
    print("Se conectó", jugador + "s")
    return "Descifraste el mensaje secreto"


def main(ip, puerto, mano):  # dirección IP, puerto, cantidad de cartas por mano
    server = crear_servidor(ip, puerto)

    lista_cartas = tarjetas.genera_lista_cartas()
    baraja = tarjetas.Baraja(lista_cartas)
    guardar_pickle(baraja, mano)

    server.register_function(prueba_conexion)
    server.register_function(pedir_mano)

    # Iniciando servidor
    print("\nIniciando servidor...\n")
    try:
        print("===========================\n")
        print("Información del servidor: ")
        print("- Servidor iniciado")
        print("- Dirección IP:", ip)
        print("- Puerto:", puerto)
        print("\n===========================")
        print("\nUsa Control-C para salir.")
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
