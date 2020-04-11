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
import tarjetas
import time


def mostrar_bienvenida(jugador, ip, puerto):
    '''
        Imprime el mensaje de bienvenida
    '''
    print("Hola, ", jugador,  "\b!")
    print("Dirección IP: ", ip)
    print("Puerto: ", puerto)


def despliega_menu():
    print("--------------------------\n")
    print("** MENU **\n")
    print("1.- Pedir mano.")
    print("2.- Mostrar jugadores.")
    print("3.- Mostrar manos de todos. (¡JUGAR!)")
    print("4.- Volver a jugar.")
    print("5.- Mostrar marcador (ver el estado del juego).")
    print("6.- Preguntas frecuentemente preguntadas. <-- ¡IMPORTANTE!")
    print("0.- Salir.")
    o = input("\nOpción:> ")

    # agregar número si agregas opción nueva
    opciones = ['1', '2', '3', '4', '5', '6', '0']
    if o in opciones:
        return int(o)
    else:
        print("Por favor, elige una opción dentro del rango de opciones.")
        return despliega_menu()


def faq():
    print("== PREGUNTAS FRECUENTEMENTE PREGUNTADAS ==\n")
    print("\n¿Qué hace la opción '1'?")
    print("     Al empezar a jugar, se entra en modo espectador.\n"
          + "Si se quiere jugar, se debe pedir una mano de la baraja.")

    print("\n¿Qué hace la opción '2'?")
    print("     Muestra a los jugadores dentro de la partida.\n"
          + "        Es necesario haber pedido cartas para aparecer aquí.")

    print("\n¿Qué hace la opción '3'?")
    print("     Muestra la mano de los 'juegadores'.\n"
          + "Teóricamente aquí se decide quién gana.               ̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\з= ( ▀ ͜͞ʖ▀) =ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿")

    print("\n¿Qué hace la opción '4'?")
    print("     Reinicia el juego. Devuelve cartas. Reinicia manos.\n"
          + "Para lograr esto, es necesario haber terminado una partida o haber pulsado '3'."
          + "Se necesita haber jugado al menos una vez."
          + "Se optó por hacer que se reiniciara la mano del jugador que presiona '4', en lugar de"
          + "hacer que todos reinicien su baraja. Por el bien de que todos estén de acuerdo de en volver a jugar.")

    print("\n¿Qué hace la opción '5'?")
    print("     Este es el marcador de la partida.\n"
          + "Muestra a los jugadores y sus victorias. (｡◕‿‿◕｡)")

    print("\n¿Qué hace la opción '6'?")
    print("     Abre un FAQ, estás dentro. ಠ_ಠ \n")

    print("\n¿Qué hace la opción '0'?")
    print("     Te saca de la partida.\n"
          + "Manda un mensaje al servidor de tu salida. Se devuelven tus cartas a la baraja.\n")

    print("( ͡° ͜ʖ ͡°)/´")

    salir = input("Presiona ENTER para salir.")


def mostrar_mano(jugador, mano):
    '''
        muestra la mano de un jugador
        recibe: nombre del jugador, uso: "Emilio"
        recibe: lista de cartas del jugador, uso: mano
    '''

    print("===========================")
    print(str(jugador) + ", tu mano es: \n")
    ordena_mano(mano)
    print("===========================\n")


def ordena_mano(mano):
    lista_mano = []
    for carta in mano:  # Se itera la mano.
        # Al ser un string, se separa cada vez que encuentre un '-'.
        carta_separada = carta.split("-")
        # Se hace un append del resultado a lista_mano
        lista_mano.append(carta_separada)

    # Se ordena lista_mano por su indice [0], uso: número de la carta.
    ordered_list = sorted(lista_mano, key=lambda numero: numero[0])

    for carta in ordered_list:
        print(carta[0], "-", carta[1])


def mostrar_jugadores(lista_jugadores):
    '''
        imprime todos los jugadores de una lista
        recibe: una lista de nombres de jugadores (str), uso: lista_jugadores
    '''
    print("* Jugadores:", str(len(lista_jugadores)) + "\n")
    i = 1
    for jugador in lista_jugadores:
        print(" - Jugador(a)", str(i) + ":", jugador)
        i += 1


def mostrar_marcador(lista_jugadores,proxy):
    '''
        Imprime los jugadores que han jugado, y las veces que han ganado. Además de la ronda en la que están.
    '''
    veces_ganadas = 0  # Esto es de mentira, se debe de hacer algo para obtener las veces ganadas de cada jugador.
    print("== MARCADOR ==\n")

    dict_marcadores, rondas = proxy.obten_partidas_ganadas()

    for nombre_jugador, partidas_ganadas in dict_marcadores.items():
        print(f"Jugador: {nombre_jugador} {partidas_ganadas} partidas ganadas")

    return rondas

    """for jugador in lista_jugadores:
        marcador = proxy.obten_partidas_ganadas(jugador)
        print("Jugador:", jugador, "(" + str(marcador) + " partidas ganadas).")"""


def mostrar_manos_todos(lista_nombres_jugadores, lista_cartas_todos, dicc_puntos):
    '''
        imprime las manos de todos los jugadores y dice quien ganó
        recibe: una lista de nombres de jugadores (str), uso: lista_jugadores
        recibe: una lista de las cartas de todos (Carta), uso: lista_cartas_todos
    '''
    if len(lista_nombres_jugadores) > 0:
        for jugador, mano in zip(lista_nombres_jugadores, lista_cartas_todos):
            mostrar_mano(jugador, mano)
            mostrar_puntaje(dicc_puntos, jugador)
            print("\n")

        # función chila que diga quién ganó aki
    else:
        print("No existen jugadores dentro de la partida. Intenta agregar algunos.")


def mostrar_puntaje(dicc_puntos, jugador):
    '''
        John Romero was here, was he?
        he ded
        tho
    '''
    for nombre_jugador, lista in dicc_puntos.items():
        if jugador == nombre_jugador:
            pares = lista[0]
            tercias = lista[1]
            puntuacion = lista[2]
            print("- Pares:", pares)
            print("- Tercias:", tercias)
            print("- Puntaje:", puntuacion)


def main(jugador, ip, puerto):
    print("\n== JUEGO DE BARAJA FRANCESA (ahora con servidor)==\n")
    print("Iniciando...\n")

    try:
        proxy = xmlrpc.client.ServerProxy(
            "http://" + str(ip) + ":" + str(puerto))
        mostrar_bienvenida(jugador, ip, puerto)
        # print(proxy.prueba_conexion(jugador))  # SOLO USAR PARA TESTING
        opcion = 666
        tiene_mano = False
        jugado = False
        mano = []
        lista_nombres_jugadores = []
        lista_cartas_todos = []
        i = 0

        while opcion != 0:
            opcion = despliega_menu()
            print("\n")
            if opcion == 1:
                if (tiene_mano == False):
                    mano = proxy.genera_mano(jugador)
                    tiene_mano = True
                    if mano != 0:
                        mostrar_mano(jugador, mano)
                    else:
                        print("No es posible dar más cartas.")
                else:
                    mostrar_mano(jugador, mano)
                    print("AVISO: ¡Ya tienes mano! No puedes cambiar de mano.\n")

            elif opcion == 2:
                lista_nombres_jugadores = proxy.mostrar_jugadores()

                if len(lista_nombres_jugadores) > 0:
                    mostrar_jugadores(lista_nombres_jugadores)
                    time.sleep(2.0)
                else:
                    print("Aún no se han agregado jugadores. Intenta agregar algunos.")
                    time.sleep(2.0)

            elif opcion == 3:
                lista = proxy.obten_mano_todos()
                lista_nombres_jugadores = lista[0]
                lista_cartas_todos = lista[1]
                #i = proxy.numero_rondas(i)
                if len(lista_nombres_jugadores) > 1:
                    #print("A")
                    lista_dos, i = proxy.obten_puntaje()
                    dicc_puntos = lista_dos[0]
                    lista_empatados = lista_dos[1]
                    mostrar_manos_todos(
                        lista_nombres_jugadores, lista_cartas_todos, dicc_puntos)
                    if len(lista_empatados) > 1:
                        # hay varios empatados
                        print("Los empatados son:")
                        for j in lista_empatados:
                            print(j)
                    else:
                        print("Ganó", lista_empatados[0])
                    #mostrar_opcion_3(dicc_puntos, jugador, mano)
                    jugado = True
                else:
                    print("No hay suficientes jugadores en la partida."
                          + " Intenta agregar más de 1.")

            elif opcion == 4:
                if jugado == True:
                    if len(mano) != 0:
                        num_cartas = len(mano)
                        mano = proxy.cambiar_mano(num_cartas, jugador)
                        tiene_mano = True
                        print("¡Nueva mano!")
                        mostrar_mano(jugador, mano)
                        print("\nCalculando las manos de los jugadores oponentes...")
                        lista = proxy.obten_mano_todos()
                        lista_nombres_jugadores = lista[0]
                        lista_cartas_todos = lista[1]
                        time.sleep(3.0)
                        if len(lista_nombres_jugadores) > 1:
                            #print("A")
                            lista_dos, i = proxy.obten_puntaje()
                            dicc_puntos = lista_dos[0]
                            lista_empatados = lista_dos[1]
                            mostrar_manos_todos(
                                lista_nombres_jugadores, lista_cartas_todos, dicc_puntos)
                            if len(lista_empatados) > 1:
                                # hay varios empatados
                                print("Los empatados son:")
                                for j in lista_empatados:
                                    print(j)
                            else:
                                print("Ganó", lista_empatados[0])
                        else:
                            print(
                                "No hay suficientes jugadores en la partida. Intenta agregar más de uno.")
                            time.sleep(3)
                    else:
                        print("No cuentas con una mano aún. Intenta pedir mano (1).")
                        time.sleep(3)
                else:
                    print("Ninguna partida ha sido iniciada por el momento.")
                    time.sleep(3)

            elif opcion == 5:
                lista_nombres_jugadores = proxy.mostrar_jugadores()

                if len(lista_nombres_jugadores) > 0:

                    i = mostrar_marcador(lista_nombres_jugadores,proxy)
                    print("Ronda: ", i)
                else:
                    print(
                        "No hay suficientes jugadores o bien, no se ha jugado una partida aún.")

            elif opcion == 6:
                faq()

        #if tiene_mano == True:  # ya tienes una mano
        #    proxy.salir(jugador)
        print("\n¡Gracias por jugar!\n")

    except ConnectionError:
        print("Ha habido un error de conexión con el servidor.\n")

    except KeyboardInterrupt:
        #if tiene_mano == True:  # ya tienes una mano
        #    proxy.salir(jugador)
        print(str(jugador) + ", haz salido de la partida.")

    except:
        print(str(jugador) + ", has salido de la partida. Tu mano ha sido devuelta a la baraja.\n"
              + "Gracias por 'JUEGAR'.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jugador', dest='jugador',
                        help="Nombre del Jugador", required=True)
    # parser.add_argument('-j', '--jugador', dest='jugador',
    #                    help="Nombre del Jugador", required=False, default="TEST")  # SOLO DEBUG
    parser.add_argument('-d', '--direccion', dest='direccion',
                        help="Dirección IP", required=False, default="localhost")
    parser.add_argument('-p', '--puerto', dest='puerto',
                        help="Puerto", required=False, default=9000)

    args = parser.parse_args()
    jugador = args.jugador
    direccion = args.direccion
    puerto = args.puerto

    main(jugador, direccion, puerto)
