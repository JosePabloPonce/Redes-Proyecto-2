import socket, os, sys
from threading import Thread
import json
from deck_of_cards import deck_of_cards
import time

HOST, PORT = '127.0.0.1', 1234
NAME = input("Ingresar Nombre: ")
conexion = ""

print("#"+"-"*30+"#")  #separator

BUFSIZE = 1024

ADDR = (HOST, PORT)

INIT_CONEX = {"request": "INIT_CONEX","body": [NAME,ADDR]}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

client_socket.send(bytes(json.dumps(INIT_CONEX), 'UTF-8'))
mensaje = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))

if (mensaje['response'] == "INIT_CONEX"):
	conexion = True

left = False

def turno(msg):
	opcion = input("1. Tomar carta y cambiarla por una del mazo\n2. Revelar carta del mazo\n3.Tomar carta desechada y cambiarla por una del mazo\n")
	for i in range (len(msg)):
				print(str(i)+". ", msg[i])
	if(opcion) == "1":
		carta =  input("Ingrese el numero de la carta que desea cambiar:\n")
	if(opcion) == "2":
		carta =  input("Ingrese el numero de la carta que desea revelar:\n")
	if(opcion) == "3":
		carta =  input("Ingrese el numero de la carta que desea cambiar:\n")
	POST_TURNO = {"request": "POST_TURNO", "body":[opcion,carta], "name": NAME}
	client_socket.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))

print("BIENVENIDO A GOLF CARD GAME \n")
opcion = input("1.Iniciar juego \n2.Salir\n")
while conexion:
	if opcion == '1':
		INICIO_JUEGO =  {"request": "INICIO_JUEGO"}
		client_socket.send(bytes(json.dumps(INICIO_JUEGO), 'UTF-8'))
		print("ESPERANDO A MAS JUGADORES...\n")
		msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
		if (msg['response'] == "INICIO_JUEGO"):
			print("JUEGO INICIADO\n")
			print("LISTA DE JUGADORES")
			print(msg['body'], "\n")
			GET_CARTAS =  {"request": "GET_CARTAS"}
			client_socket.send(bytes(json.dumps(GET_CARTAS), 'UTF-8'))
			msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
			print("BARAJA DE CARTAS")
			print(msg['body'], "\n")
			print("Selecciona las dos cartas que deseas mostrar:\n")
			for i in range (len(msg['body'][0])):
				print(str(i)+". ", msg['body'][0][i])
			carta1 = input("Ingrese el numero de la carta 1:\n")
			carta2 = input("Ingrese el numero de la carta 2:\n")
			POST_CARTA_INI = {"request": "POST_CARTA_INI", "body" : [carta1,carta2], "name": NAME}
			client_socket.send(bytes(json.dumps(POST_CARTA_INI), 'UTF-8'))
			msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
			print("BARAJA DE CARTAS")
			print(msg['body'], "\n")
			mazo_recibido = (msg['body'][0])
			GET_TURNO = {"request": "GET_TURNO"}
			client_socket.send(bytes(json.dumps(GET_TURNO), 'UTF-8'))
			print("ESPERANDO TURNO...")
			msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
			turno_jugador = msg["body"][0]
			continuar_juego = msg["body"][1]
			
			while (continuar_juego):
				while(turno_jugador != NAME):
					print("ESPERANDO TURNO...")
					time.sleep(15)
					client_socket.send(bytes(json.dumps(GET_TURNO), 'UTF-8'))
					msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
					if(msg['response'] == 'GET_TURNO'):
						turno_jugador = msg["body"][0]
						continuar_juego = msg["body"][1]

					else:
						pass

				
				if(continuar_juego == False):
					continue

				
				turno(mazo_recibido)
				msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
				print(msg)
				mazo_recibido = (msg['body'][0])

				GET_TURNO = {"request": "GET_TURNO"}
				client_socket.send(bytes(json.dumps(GET_TURNO), 'UTF-8'))
				msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
				turno_jugador = msg["body"][0]
				continuar_juego = msg["body"][1]

			print("JUEGO FINALIZADO")
			for i in range (len(mazo_recibido)):
				print(str(i)+". ", mazo_recibido[i])
			extra = input("Desea cambiar una carta de su mazo por la carta extra?\n1. Si\n2. No\n")

			if(extra == "1"):
				carta_extra = input("Ingrese la posicion de la carta que desea cambiar:\n")
				POST_CARTAEXTRA = {
				"request": "POST_CARTAEXTRA",
				"body": carta_extra,
				"name": NAME
				}
				client_socket.send(bytes(json.dumps(POST_CARTAEXTRA), 'UTF-8'))
				msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
				mazo_recibido = msg['body']
			if(extra == "2"):
				POST_NOCARTAEXTRA = {
				"request": "POST_NOCARTAEXTRA",
				"name": NAME
				}
				client_socket.send(bytes(json.dumps(POST_CARTAEXTRA), 'UTF-8'))
				msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
				mazo_recibido = msg['body']

			print(mazo_recibido)
			



	if opcion == '2':
		END_CONEX = {"request": "END_CONEX"}
		left = True
		client_socket.send(bytes(json.dumps(END_CONEX), 'UTF-8'))
		client_socket.close()
		sys.exit()
		break