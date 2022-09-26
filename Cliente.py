import socket, os, sys
from threading import Thread

HOST, PORT = '127.0.0.1', 1234
NAME = input("Ingresar Nombre: ")

print("#"+"-"*30+"#")  #separator

BUFSIZE = 1024

ADDR = (HOST, PORT)

RESET = "\033[0;0m"
BOLD  = "\033[;1m"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

client_socket.send(bytes(NAME, "utf-8"))

left = False

def rc(): #rc > recieve
	while True:
		try:
			msg = client_socket.recv(BUFSIZE).decode("utf-8")
			if not left:
				sys.stdout.write("\r\033[K")
				sys.stdout.write(msg), sys.stdout.flush()
				sys.stdout.write("\r\033[K")
				sys.stdout.write(BOLD+"{}> ".format(NAME)+RESET); sys.stdout.flush()

		except:
			break

sys.stdout.write(BOLD+"Welcome {}. Puedes empezar a enviar mensajes!".format(NAME)+RESET+"\n")

while True:
	x = Thread(target=rc)
	x.start()
	sys.stdout.write("\r\033[K")
	sys.stdout.write(BOLD+"{}> ".format(NAME)+RESET); sys.stdout.flush()
	msg = sys.stdin.readline()
	if msg == "/quit\n":
		left = True
		client_socket.send(bytes("LEFT", "utf-8"))
		client_socket.close()
		sys.exit()
		break
	elif msg == "/list\n":
		client_socket.send(bytes("LIST", "utf-8"))
		continue
	client_socket.send(bytes(msg, "utf-8"))