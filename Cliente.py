import socket, os, sys
from threading import Thread
import json
from deck_of_cards import deck_of_cards

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
			#for i in range(3):
			client_socket.send(bytes(json.dumps(POST_CARTA_INI), 'UTF-8'))
			msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
			print("BARAJA DE CARTAS")
			print(msg['body'], "\n")
			turno(msg['body'][0])
			msg = json.loads(client_socket.recv(BUFSIZE).decode('UTF-8'))
			print(msg)

	if opcion == '2':
		END_CONEX = {"request": "END_CONEX"}
		left = True
		client_socket.send(bytes(json.dumps(END_CONEX), 'UTF-8'))
		client_socket.close()
		sys.exit()
		break