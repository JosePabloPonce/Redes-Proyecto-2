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

msg = ""

def rc():
	global msg
	while True:
		try:
			msg = json.loads(client_socket.recv(BUFSIZE).decode("utf-8"))
			if(msg==""):
				print("vacio")
		except:
			break

def turno(msg):
	opcion = input("1. Tomar carta y cambiarla por una del mazo\n2. Revelar carta del mazo\n3.Tomar carta desechada y cambiarla por una del mazo\n")
	for i in range (len(msg)):
			if (i != 0 or i != 7):
				print(str(i)+". ", msg[i])
	if(opcion) == "1":
		carta =  input("Ingrese el numero de la carta que desea cambiar:\n")
	if(opcion) == "2":
		carta =  input("Ingrese el numero de la carta que desea revelar:\n")
	if(opcion) == "3":
		carta =  input("Ingrese el numero de la carta que desea cambiar:\n")
	if(opcion) == "4":
		carta =  input("Ingrese el numero de la carta que desea cambiar:\n")
	POST_TURNO = {"request": "POST_TURNO", "body":[opcion,carta], "name": NAME}
	client_socket.send(bytes(json.dumps(POST_TURNO), 'UTF-8'))

print("BIENVENIDO A GOLF CARD GAME \n")
opcion = input("1.Iniciar juego \n2.Salir\n")
while conexion:
	if opcion == '1':
		x = Thread(target=rc)
		x.start()
		INICIO_JUEGO =  {"request": "INICIO_JUEGO"}
		client_socket.send(bytes(json.dumps(INICIO_JUEGO), 'UTF-8'))
		print("ESPERANDO A MAS JUGADORES...\n")		
		while(msg == ""):
			for i in  range(100):
				i
			if(msg != ""):
				while(msg['response'] != "INICIO_JUEGO"):
					msg
		if (msg['response'] == "INICIO_JUEGO"):
			print("JUEGO INICIADO\n")
			print("LISTA DE JUGADORES")
			print(msg['body'], "\n")
			GET_CARTAS =  {"request": "GET_CARTAS"}
			client_socket.send(bytes(json.dumps(GET_CARTAS), 'UTF-8'))
			while(msg['response'] != "GET_CARTAS"):
				msg
			print("BARAJA DE CARTAS")
			print(msg['body'], "\n")
			print("Selecciona las dos cartas que deseas mostrar:\n")
			for i in range (len(msg['body'][0])):
				if (i != 0 or i != 7):
					print(str(i)+". ", msg['body'][0][i])
			carta1 = input("Ingrese el numero de la carta 1:\n")
			carta2 = input("Ingrese el numero de la carta 2:\n")
			POST_CARTA_INI = {"request": "POST_CARTA_INI", "body" : [carta1,carta2], "name": NAME}
			#for i in range(3):
			client_socket.send(bytes(json.dumps(POST_CARTA_INI), 'UTF-8'))
			while(msg['response'] != "POST_CARTA_INI"):
				msg
			print("BARAJA DE CARTAS")
			print(msg['body'], "\n")
			mazo_recibido = (msg['body'])
			GET_TURNO = {"request": "GET_TURNO"}
			client_socket.send(bytes(json.dumps(GET_TURNO), 'UTF-8'))
			print("ESPERANDO TURNO...")
			while(msg['response'] != "GET_TURNO"):
				msg
			turno_jugador = msg["body"][0]
			continuar_juego = msg["body"][1]
			
			while (continuar_juego):
				while(turno_jugador != NAME):
					print("ESPERANDO TURNO...")
					time.sleep(15)
					client_socket.send(bytes(json.dumps(GET_TURNO), 'UTF-8'))
					while(msg['response'] != "GET_TURNO"):
						msg
					if(msg['response'] == 'GET_TURNO'):
						turno_jugador = msg["body"][0]
						continuar_juego = msg["body"][1]
					else:
						pass

				
				if(continuar_juego == False):
					continue

				for i in range(3):
					if(NAME == mazo_recibido[i][0][0]):
						turno(mazo_recibido[i][0])

				while(msg['response'] != "POST_TURNO"):
						msg
				print(msg)
				mazo_recibido = (msg['body'][0])

				GET_TURNO = {"request": "GET_TURNO"}
				client_socket.send(bytes(json.dumps(GET_TURNO), 'UTF-8'))
				while(msg['response'] != "GET_TURNO"):
						msg
				turno_jugador = msg["body"][0]
				continuar_juego = msg["body"][1]

	if opcion == '2':
		END_CONEX = {"request": "END_CONEX"}
		left = True
		client_socket.send(bytes(json.dumps(END_CONEX), 'UTF-8'))
		client_socket.close()
		sys.exit()
		break