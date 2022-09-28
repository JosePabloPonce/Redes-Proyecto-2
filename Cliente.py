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

while conexion:
	print("BIENVENIDO A GOLF CARD GAME \n")
	opcion = input("1.Iniciar juego \n2.Salir\n")
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

	if opcion == '2':
		END_CONEX = {"request": "END_CONEX"}
		left = True
		client_socket.send(bytes(json.dumps(END_CONEX), 'UTF-8'))
		client_socket.close()
		sys.exit()
		break