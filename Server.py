import socket, os, sys
from threading import Thread
import json

HOST, PORT = '127.0.0.1', 1234

BUFSIZ = 1024
ADDR = (HOST, int(PORT))

RESET = "\033[0;0m"
BOLD  = "\033[;1m"
RED  = "\033[91m"
GREEN = "\033[92m"

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

SERVER.listen(1)

#functon that converts a list into a string with separator: ';'
#['hi', 'my', 'name', 'is'] becomes hi;my;name;is

def convert_list(lista):
	string = ""
	for item in lista:
		string += item+";"
	string += "\n"
	l = list(string)
	del l[-2]
	string = ""
	for item in l:
		string += item
	return string

def from_client(client, adress):
	while True:
		try:
			msg = json.loads(client.recv(BUFSIZ).decode('UTF-8'))
			if(mensaje['request'] == "INICIO_JUEGO"):
				print("a")

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
		c.send(bytes(json.dumps(INIT_CONEX), 'UTF-8'))
	
	#for sock in lista_sockets:
	#	sock.send(bytes("INFO: "+BOLD+GREEN+a[0]+":"+str(a[1])+" ("+"%s" % (name) +")"+" Se unio"+RESET+"\n", "utf-8"))
	
	Thread(target=from_client, args=(c,a)).start()
	#print(Nombres, people)