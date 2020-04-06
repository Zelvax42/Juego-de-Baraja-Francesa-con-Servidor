#!/usr/bin/python

# Equipo: Mustafar
# Fecha: 10 de abril de 2020
# Integrantes:
#
#   Félix López Juan Pablo
#   López Velásquez Octavio
#   Serna Navarro Ángel Emilio
'''
    Cliente baraja
    Programa: cliente_baraja.
'''

import xmlrpc.client
import argparse
import servidor_baraja
import copy
import time


def despliega_menu():
    print("--------------------------\n")
    print("** MENU **\n")
    print("1.- Pedir mano")
    print("2.- Mostrar jugadores")
    print("3.- Mostrar manos de todos")
    print("4.- Volver a jugar")
    print("5.- Mostrar marcador")
    print("0.- Salir")
    o = input("\nOpción:> ")

    opciones = ['1','2','3','4','5','0']
    if o in opciones:
        return int(o)
    else:
        print("¡Opción incorrecta!")
        return despliega_menu()


def main(jugador, ip, puerto):
    print("\n== JUEGO DE BARAJA FRANCESA ==\n")
    print("Iniciando...\n")

    try:        
        proxy = xmlrpc.client.ServerProxy("http://" + str(ip) + ":" + str(puerto))
        #print(proxy.prueba_conexion(jugador))  # SOLO USAR PARA TESTING
        opcion = 10930193413
        while opcion != 0:
            opcion = despliega_menu()
            print("\n")
            if opcion == 0:
                pass
            elif opcion == 1:
                pass
            elif opcion == 2:
                pass
            elif opcion == 3:
                pass
            elif opcion == 4:
                pass
            elif opcion == 5:
                pass
        print("\n¡Gracias por jugar!\n")
    except ConnectionError:
        print("Error de conexión con el servidor.\n")
    except KeyboardInterrupt:
        print("Cancelado por el usuario")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jugador', dest='jugador',
                        help="Nombre del Jugador", required=True)
    parser.add_argument('-d', '--direccion', dest='direccion',
                        help="Dirección IP", required=False, default="localhost")
    parser.add_argument('-p', '--puerto', dest='puerto',
                        help="Puerto", required=False, default=9000)

    args = parser.parse_args()
    jugador = args.jugador
    direccion = args.direccion
    puerto = args.puerto

    main(jugador, direccion, puerto)
