import socket, os, sys
from threading import Thread
import json
from deck_of_cards import deck_of_cards

HOST, PORT = 'https://golf-server-proyecto.herokuapp.com/', 1234

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
sala1_jugadores_cartas_nombres_oculta = []
sala1_contador_turno = 0
sala1_contador_turno_inicial = 0
sala1_contador_turno_inicial2 = 0
sala1_continua_juego = True

def from_client(client, adress, nombre):
	global sala1_continua_juego
	global sala1_contador_turno 
	global sala1_contador_turno_inicial 
	global sala1_contador_turno_inicial2
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
				lista_temporal1 = [nombre]
				lista_temporal2 = [nombre]
				lista_temporal3 = [nombre]
				for i in range (0, 7):
					carta = sala1_baraja.give_random_card()
					lista_temporal1.append(carta.name)
					lista_temporal2.append(carta.value)
					lista_temporal3.append(carta.suit)
					if(i == 6):
						sala1_jugadores_cartas_nombres_oculta.append([[nombre, 0,0,0,0,0,0, carta.name]])
				sala1_jugadores_cartas_nombres.append(lista_temporal1)
				sala1_jugadores_cartas_valores.append(lista_temporal2)
				sala1_jugadores_cartas_palo.append(lista_temporal3)
				sala1_jugadores_cartas_palo
				GET_CARTAS = {"response": "GET_CARTAS", "body": sala1_jugadores_cartas_nombres_oculta[len(sala1_jugadores_cartas_nombres_oculta)-1]}
				client.send(bytes(json.dumps(GET_CARTAS), 'UTF-8'))
			if(msg['request'] == "POST_CARTA_INI"):
				cartas = msg['body']
				name = msg['name']
				if(name == sala1_jugadores_cartas_nombres_oculta[0][0][0]):
					sala1_jugadores_cartas_nombres_oculta[0][0][int(cartas[0])] = sala1_jugadores_cartas_nombres[0][int(cartas[0])]
					sala1_jugadores_cartas_nombres_oculta[0][0][int(cartas[1])] = sala1_jugadores_cartas_nombres[0][int(cartas[1])]
					POST_CARTA_INI = {"response": "POST_CARTA_INI", "body" : sala1_jugadores_cartas_nombres_oculta[0]}
					client.send(bytes(json.dumps(POST_CARTA_INI), 'UTF-8'))
				if(name == sala1_jugadores_cartas_nombres_oculta[1][0][0]):
					sala1_jugadores_cartas_nombres_oculta[1][0][int(cartas[0])] = sala1_jugadores_cartas_nombres[1][int(cartas[0])]
					sala1_jugadores_cartas_nombres_oculta[1][0][int(cartas[1])] = sala1_jugadores_cartas_nombres[1][int(cartas[1])]
					POST_CARTA_INI = {"response": "POST_CARTA_INI", "body" : sala1_jugadores_cartas_nombres_oculta[1]}
					client.send(bytes(json.dumps(POST_CARTA_INI), 'UTF-8'))
				if(name == sala1_jugadores_cartas_nombres_oculta[2][0][0]):
					sala1_jugadores_cartas_nombres_oculta[2][0][int(cartas[0])] = sala1_jugadores_cartas_nombres[2][int(cartas[0])]
					sala1_jugadores_cartas_nombres_oculta[2][0][int(cartas[1])] = sala1_jugadores_cartas_nombres[2][int(cartas[1])]
					POST_CARTA_INI = {"response": "POST_CARTA_INI", "body" : sala1_jugadores_cartas_nombres_oculta[2]}
					client.send(bytes(json.dumps(POST_CARTA_INI), 'UTF-8'))
			
			if(msg['request'] == "GET_TURNO"):


				GET_TURNO = {"response": "GET_TURNO", "body" : [sala1_Jugadores[sala1_contador_turno], sala1_continua_juego] }

				if(sala1_contador_turno_inicial2 != 0):
					client.send(bytes(json.dumps(GET_TURNO), 'UTF-8'))

				if(sala1_contador_turno_inicial < 3):
					sala1_contador_turno_inicial +=1
				
				if (sala1_contador_turno_inicial == 3 and sala1_contador_turno_inicial2 == 0):
					
					for sock in sala1_sockets:
						sock.send(bytes(json.dumps(GET_TURNO), 'UTF-8'))
						sala1_contador_turno_inicial2 +=1
				
			if(msg['request'] == "POST_TURNO"):
				sala1_contador_turno += 1
				if(sala1_contador_turno == 3):
					sala1_contador_turno = 0

				opcion = msg['body'][0]
				name = msg['name']
				carta = msg['body'][1]
				card = sala1_baraja.give_random_card()
				if(opcion == "1"):
					if(name == sala1_jugadores_cartas_nombres_oculta[0][0][0]):
						desecho = sala1_jugadores_cartas_nombres[0][int(carta)]
						sala1_jugadores_cartas_nombres_oculta[0][0][int(carta)] = card.name
						sala1_jugadores_cartas_nombres[0][int(carta)] = card.name
						POST_TURNO = {"response": "POST_TURNO", "body" : sala1_jugadores_cartas_nombres_oculta[0], "desecho": desecho}
						client.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))
						if 0 not in sala1_jugadores_cartas_nombres_oculta[0][0]:
							sala1_continua_juego = False

					if(name == sala1_jugadores_cartas_nombres_oculta[1][0][0]):
						desecho = sala1_jugadores_cartas_nombres[1][int(carta)]
						sala1_jugadores_cartas_nombres_oculta[1][0][int(carta)] = card.name
						sala1_jugadores_cartas_nombres[1][int(carta)] = card.name
						POST_TURNO = {"response": "POST_TURNO", "body" : sala1_jugadores_cartas_nombres_oculta[1], "desecho": desecho}
						client.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))
						if 0 not in sala1_jugadores_cartas_nombres_oculta[1][0]:
							sala1_continua_juego = False

					if(name == sala1_jugadores_cartas_nombres_oculta[2][0][0]):
						desecho = sala1_jugadores_cartas_nombres[2][int(carta)]
						sala1_jugadores_cartas_nombres_oculta[2][0][int(carta)] = card.name
						sala1_jugadores_cartas_nombres[2][int(carta)] = card.name
						POST_TURNO = {"response": "POST_TURNO", "body" : sala1_jugadores_cartas_nombres_oculta[2], "desecho": desecho}
						client.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))
						if 0 not in sala1_jugadores_cartas_nombres_oculta[2][0]:
							sala1_continua_juego = False

				if(opcion == "2"):
					if(name == sala1_jugadores_cartas_nombres_oculta[0][0][0]):
						desecho = card.name
						sala1_jugadores_cartas_nombres_oculta[0][0][int(carta)] = sala1_jugadores_cartas_nombres[0][int(carta)]
						POST_TURNO = {"response": "POST_TURNO", "body" : sala1_jugadores_cartas_nombres_oculta[0], "desecho": desecho}
						client.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))
						if 0 not in sala1_jugadores_cartas_nombres_oculta[0][0]:
							sala1_continua_juego = False

					if(name == sala1_jugadores_cartas_nombres_oculta[1][0][0]):
						desecho = card.name
						sala1_jugadores_cartas_nombres_oculta[1][0][int(carta)] = sala1_jugadores_cartas_nombres[1][int(carta)]
						POST_TURNO = {"response": "POST_TURNO", "body" : sala1_jugadores_cartas_nombres_oculta[1], "desecho": desecho}
						client.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))
						if 0 not in sala1_jugadores_cartas_nombres_oculta[1][0]:
							sala1_continua_juego = False

					if(name == sala1_jugadores_cartas_nombres_oculta[2][0][0]):
						desecho = card.name
						sala1_jugadores_cartas_nombres_oculta[2][0][int(carta)] = sala1_jugadores_cartas_nombres[2][int(carta)]
						POST_TURNO = {"response": "POST_TURNO", "body" : sala1_jugadores_cartas_nombres_oculta[2], "desecho": desecho}
						client.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))
						if 0 not in sala1_jugadores_cartas_nombres_oculta[2][0]:
							sala1_continua_juego = False

				if(opcion == "3"):
					if(name == sala1_jugadores_cartas_nombres_oculta[0][0][0]):
						sala1_jugadores_cartas_nombres_oculta[0][0][int(carta)] = desecho
						sala1_jugadores_cartas_nombres[0][int(carta)] = desecho
						POST_TURNO = {"response": "POST_TURNO", "body" : sala1_jugadores_cartas_nombres_oculta[0], "desecho": desecho}
						client.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))
						if 0 not in sala1_jugadores_cartas_nombres_oculta[2][0]:
							sala1_continua_juego = False
					if(name == sala1_jugadores_cartas_nombres_oculta[1][0][0]):
						sala1_jugadores_cartas_nombres_oculta[1][0][int(carta)] = desecho
						sala1_jugadores_cartas_nombres[1][int(carta)] = desecho
						POST_TURNO = {"response": "POST_TURNO", "body" : sala1_jugadores_cartas_nombres_oculta[1], "desecho": desecho}
						client.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))
						if 0 not in sala1_jugadores_cartas_nombres_oculta[2][0]:
							sala1_continua_juego = False
					if(name == sala1_jugadores_cartas_nombres_oculta[2][0][0]):
						sala1_jugadores_cartas_nombres_oculta[2][0][int(carta)] = desecho
						sala1_jugadores_cartas_nombres[2][int(carta)] = desecho
						POST_TURNO = {"response": "POST_TURNO", "body" : sala1_jugadores_cartas_nombres_oculta[2], "desecho": desecho}
						client.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))
						if 0 not in sala1_jugadores_cartas_nombres_oculta[2][0]:
							sala1_continua_juego = False
			if(msg['request'] == "POST_CARTAEXTRA"):
				carta = msg['body']
				name = msg['name']
				if(name == sala1_jugadores_cartas_nombres_oculta[0][0][0]):
					sala1_jugadores_cartas_nombres[0][int(carta)] = sala1_jugadores_cartas_nombres_oculta[0][0][7]
					POST_CARTAEXTRA = {"response": "POST_CARTAEXTRA", "body" : sala1_jugadores_cartas_nombres[0]}
					client.send(bytes(json.dumps(POST_CARTAEXTRA), 'UTF-8'))

				if(name == sala1_jugadores_cartas_nombres_oculta[1][0][0]):
					sala1_jugadores_cartas_nombres[1][int(carta)] = sala1_jugadores_cartas_nombres_oculta[1][0][7]
					POST_CARTAEXTRA = {"response": "POST_CARTAEXTRA", "body" : sala1_jugadores_cartas_nombres[1]}
					client.send(bytes(json.dumps(POST_CARTAEXTRA), 'UTF-8'))

				if(name == sala1_jugadores_cartas_nombres_oculta[2][0][0]):
					sala1_jugadores_cartas_nombres[2][int(carta)] = sala1_jugadores_cartas_nombres_oculta[2][0][7]
					POST_CARTAEXTRA = {"response": "POST_CARTAEXTRA", "body" : sala1_jugadores_cartas_nombres[2]}
					client.send(bytes(json.dumps(POST_CARTAEXTRA), 'UTF-8'))

			if(msg['request'] == "POST_NOCARTAEXTRA"):
				name = msg['name']
				if(name == sala1_jugadores_cartas_nombres_oculta[0][0][0]):
					POST_NOCARTAEXTRA = {"response": "POST_NOCARTAEXTRA", "body" : sala1_jugadores_cartas_nombres[0]}
					client.send(bytes(json.dumps(POST_NOCARTAEXTRA), 'UTF-8'))

				if(name == sala1_jugadores_cartas_nombres_oculta[1][0][0]):
					POST_NOCARTAEXTRA = {"response": "POST_NOCARTAEXTRA", "body" : sala1_jugadores_cartas_nombres[1]}
					client.send(bytes(json.dumps(POST_NOCARTAEXTRA), 'UTF-8'))

				if(name == sala1_jugadores_cartas_nombres_oculta[2][0][0]):
					POST_NOCARTAEXTRA = {"response": "POST_NOCARTAEXTRA", "body" : sala1_jugadores_cartas_nombres[2]}
					client.send(bytes(json.dumps(POST_NOCARTAEXTRA), 'UTF-8'))



			if(msg['request'] == "END_CONEX"):
				sys.stdout.write(BOLD+GREEN+a[0]+":"+str(adress[1])+" Se desconecto"+RESET+"\n")
				client.close()

		except Exception as e:
			print("While loop exit because of {}".format(e)) #To remove
			client.close()
			break


print("#"+"-"*30+"#") 
print("Esperando Conexiones...")

while True:
	c, a = SERVER.accept()
	mensaje = json.loads(c.recv(BUFSIZ).decode('UTF-8'))
	sys.stdout.write(BOLD+GREEN+a[0]+":"+str(a[1])+" Conectado"+RESET+"\n")
	if (mensaje['request'] == "INIT_CONEX"):
		INIT_CONEX = {"response": "INIT_CONEX"}
		nombre = mensaje["body"][0]
		c.send(bytes(json.dumps(INIT_CONEX), 'UTF-8'))
	
	Thread(target=from_client, args=(c,a,nombre)).start()
