# :telephone_receiver: Proyecto2Redes
El proyecto consiste en implementar un juego de cartas online multijugador que utilice un protocolo 
propietario (desarrollado por el equipo) para la sincronización de los distintos clientes de este. El 
juego debe: 
- Soportar 3+ jugadores. 
- Permitir estrategia por parte de los participantes (no estar dado exclusivamente por el azar como Guerra). 
- Tener un estado público y un estado privado por jugador (no ser de información perfecta). 
- Estar basado en turnos (no ser concurso de velocidad como Speed). 
- Permitir chatear entre los jugadores. 
- Permitir elegir un nombre al momento de unirse. 
- Poder manejar varias “mesas” o “salas”. Es decir, soportar juegos concurrentes que puedan ocurrir en el servidor. 

# GOLF 
El juego implementado en este laboratorio fue golf, el consiste en utilizar una baraja de cartas de poker, en donde inicialmente a cada jugador se le dan 7 cartas que no pueden voltear, solo deben voltear una carta y guardarla para el final sin enseñarla a los demás jugadores. Las otras 6 cartas deben estar volteadas sobre el campo de juego y los jugadores inicialmente deben darle vuelta a dos cartas y ver el valor en puntos que estas tienen, el juego consiste en que las 6 cartas que están en el campo de juego sumen la menor cantidad de puntos posible. Luego de darle vuelta a las cartas cada jugador por turnos debe tomar una del manojo y decidir si cambiarla por una de sus cartas en el campo. El juego termina cuando uno de los jugadores le da vuelta a todas sus cartas, entonces todos los jugadores deben darle vuelta a sus cartas teniendo la posibilidad de cambiar una de las que tienen en campo por la que guardaron inicialmente. 

Los puntos asignados a cada carta son los siguientes: 
A -> 1
2 -> -2
K -> 0
3 a 9 -> Valor de carta
10 -> 10
J -> 10
Q -> 10
