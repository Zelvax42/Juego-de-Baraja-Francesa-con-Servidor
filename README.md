# Juego-de-Piedra-Papel-o-Tijera-con-Servidor

En esta tarea, deben lograr que funcione correctamente el siguiente juego interactivo de baraja francesa, el cual consta de dos programas, uno Servidor y otro Cliente. El Servidor lleva registro de todos los jugadores, sus “manos” y la baraja, mientras que el Cliente sirve para interactuar con el Servidor, ya sea pidiendo una nueva jugada, mostrando cuantos jugadores hay en línea, y cuál es el status del juego.

Para iniciar el juego, es necesario que el servidor servidor_baraja.py se esté ejecutando en una terminal:

 

./servidor_baraja.py -d 127.0.0.1 -p 9000 -m 5

 

Donde -d o --direccion representa la dirección IP que va a escuchar y -p o --puerto representa el puerto donde se dará la comunicación. Pueden dejar la dirección IP “0.0.0.0” como default, para poder escuchar cualquier computadora en el Internet. (Nota: necesitan redirigir el puerto que escojan en el Firewall de su módem a la dirección de la computadora que tendrá servidor_baraja.py ejecutándose). La opción -m indica el número de cartas a repartir en la "mano". (Incluyan un filtro para no pasar de repartir 52 cartas!):

Una vez que se esté ejecutando el servidor_baraja.py, se podrán abrir dos terminales y en cada una de ellas ejecutar cliente_baraja.py. El usuario iniciará el programa con el siguiente comando:

 

   ./cliente_baraja.py -j nombre_de_jugador -d 127.0.0.1 -p 9000

 

Donde -d o --direccion representa la dirección IP del servidor y -p o --puerto representa el puerto donde se dará la comunicación. Si dejan 127.0.0.1 tanto en el servidor como el cliente, podrán comunicarse los programas que se ejecuten solo en la misma computadora. Es imperativo que el puerto sea el mismo.

 

El programa cliente se conectará con el servidor y mostrará un menú de opciones al jugador, similar a este:

 

JUEGO DE PARES

MENÚ

-------

1.Pedir Mano

2.Mostrar jugadores

3.Mostrar manos de todos

4.Volver a jugar

5.Mostrar marcador

0.Salir

 

La opción 1, “Pedir mano”, el programa se conectará al servidor y éste en forma aleatoria le asignará la “mano” al jugador (removiendo las cartas entregadas de la baraja) y le devolverá la “mano” al cliente. Con esta información, se imprimirá el nombre del jugador y su mano en la siguiente forma (ordenada):

   Ana

   ---------- 

   3-P 

   4-T 

   7-P 

  10-P 

   K-C   

 

En la opción 2, “Mostrar jugadores”, el programa se conectará al servidor y éste devolverá una lista con los nombres de los jugadores. El cliente mostrará algo similar a:

Jugadores: 2

Jugador 1: Ana

Jugador 2: Beto

 

En la opción 3, “Mostrar manos de todos”, el programa se conectará al servidor y éste devolverá un diccionario con los jugadores y sus “manos”. El cliente mostrará el nombre de cada jugador por arriba de su “mano” (listada en forma ordenada) así como el puntaje de cada uno y deberá nombrar al ganador o si hubo empate. Además, debe enviar al servidor el nombre del ganador, para que este lleve cuenta en un diccionario cuantos juegos ha ganado cada jugador.

   Ana

   ---------- 

   3-P 

   4-T 

   7-P 

  10-P 

   K-C

  

   Beto

   ---------- 

   2-T 

   4-D 

   5-D 

   5-T

   10-C 

   Jugador: Beto gano con 1 par

 

Para este juego solo valdrán los pares y los tríos de cartas.

Muy importante: un par de 10s le gana a un par de 5s. Dos pares le ganan a 1 par.

 

Opción 4, “Volver a jugar”, se conecta al servidor y se reinicia la baraja, se limpian las manos.

 

Opción 5. “Mostrar marcardor”, el cliente se conecta al servidor y le pide el diccionario de marcador, y al recibirlo, lo muestra, así como la cantidad de juegos jugados:

 

Marcador:

------------

Ana: 1

Beto: 0

Juegos jugados: 1

 

Opción 0, “Salir”, el cliente se desconecta del servidor y sale.

 

La baraja francesa consta de 52 cartas distribuidas en 4 palos (corazones, diamantes, picas y tréboles), estos palos o conjuntos están conformados así: 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack (paje), Queen (reina), King (rey) y Ace (as).  Para este ejercicio, Jack tendrá un valor de 11, Queen 12, King 13 y Ace 20.

 

Es necesario hacer un archivo tarjetas.py el cual contendrá 3 clases:

 

Jugador 

(atributos: nombre (str), mano (lista) ) 

(métodos: __init__, despliega_mano() )

 

Carta 

(atributos: valor (int), figura (str)) 

(métodos: __init__, __str__ )

 

Baraja 

(atributos: diccionario de cartas ( cara:valor ), figuras (Corazones, Pinos, Tréboles, Diamantes), lista de cartas (52 en total), lista de jugadores) 

(métodos: __init__, genera_mano, guarda_jugador)

 

Es necesario que tanto el servidor, como el cliente, importen la librería tarjetas.py.

 

Rúbrica:

servidor_baraja.py

Función mano 2

Función mostrar_jugadores 2

Función mostrar_mano 2

Función mostrar_marcador 2

Argumento ip 1

Argumento puerto 1

Argumento mano 1

subtotal 11

 

cliente_baraja.py

 

Conexión al servidor 1

Menú 1

Mostrar mano 1

Mostrar jugadores 1

Mostrar manos de todos los jugadores 2

Mostrar ganador 2

Mostrar marcador 2

Reinicio del juego 2

Argumento ip 1

Argumento puerto 1

subtotal 14

Total 25
