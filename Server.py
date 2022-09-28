import socket, os, sys
from threading import Thread
import json
from deck_of_cards import deck_of_cards

HOST, PORT = '127.0.0.1', 1234

BUFSIZ = 1024
ADDR = (HOST, int(PORT))

RESET = "\033[0;0m"
BOLD  = "\033[;1m"
GREEN = "\033[92m"

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

SERVER.listen(1)

sala1_sockets = []
sala1_Jugadores = []
sala1_baraja = deck_of_cards.DeckOfCards()
sala1_jugadores_cartas_nombres = []
sala1_jugadores_cartas_valores = []
sala1_jugadores_cartas_palo = []


def from_client(client, adress, nombre):
	while True:
		try:
			msg = json.loads(client.recv(BUFSIZ).decode('UTF-8'))
			if(msg['request'] == "INICIO_JUEGO"):
				sala1_sockets.append(client)
				sala1_Jugadores.append(nombre)
				if (len(sala1_sockets) == 3):
					INICIO_JUEGO = {"response": "INICIO_JUEGO", "body": sala1_Jugadores}
					for sock in sala1_sockets:
						sock.send(bytes(json.dumps(INICIO_JUEGO), 'UTF-8'))
			
			if(msg['request'] == "GET_CARTAS"):
				lista_temporal1 = [client]
				lista_temporal2 = [client]
				lista_temporal3 = [client]
				for i in range (0, 7):
					carta = sala1_baraja.give_random_card()
					lista_temporal1.append(carta.name)
					lista_temporal2.append(carta.value)
					lista_temporal3.append(carta.suit)
				sala1_jugadores_cartas_nombres.append(lista_temporal1)
				sala1_jugadores_cartas_valores.append(lista_temporal2)
				sala1_jugadores_cartas_palo.append(lista_temporal3)
				GET_CARTAS = {"response": "GET_CARTAS", "body": sala1_jugadores_cartas_nombres}
				print(sala1_jugadores_cartas_nombres)
				client.send(bytes(json.dumps(INICIO_JUEGO), 'UTF-8'))

		except Exception as e:
			print("While loop exit because of {}".format(e)) #To remove
			client.close()
			break

people = {} #dictionary of PIDs and Nombres
Nombres = []  #list of Nombres
lista_sockets = []    #list of sockets

print("#"+"-"*30+"#") #separator

print("Esperando Conexiones...")
while True:
	c, a = SERVER.accept()
	lista_sockets.append(c)
	mensaje = json.loads(c.recv(BUFSIZ).decode('UTF-8'))
	print(mensaje)
	sys.stdout.write(BOLD+GREEN+a[0]+":"+str(a[1])+" Conectado"+RESET+"\n")
	people[a[1]] = mensaje
	Nombres.append(mensaje)
	if (mensaje['request'] == "INIT_CONEX"):
		INIT_CONEX = {"response": "INIT_CONEX"}
		nombre = mensaje["body"][0]
		c.send(bytes(json.dumps(INIT_CONEX), 'UTF-8'))
	
	#for sock in lista_sockets:
	#	sock.send(bytes("INFO: "+BOLD+GREEN+a[0]+":"+str(a[1])+" ("+"%s" % (name) +")"+" Se unio"+RESET+"\n", "utf-8"))
	
	Thread(target=from_client, args=(c,a,nombre)).start()
	#print(Nombres, people)