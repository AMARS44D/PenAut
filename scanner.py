# run with sudo
import sys
import socket

from tabulate import tabulate # pour affichage self.macList
# sudo apt install python3-tabulate / python -m pip install tabulate
from scapy.all import Ether, ARP, srp
# sudo apt install python3-scapy / python -m pip install scapy

class Port_scanner:
    def __init__(self, ip):
        self.target = ip
        self.port = range(1, 65535)
        self.port_ouvert = []

    def scan_port(self):
        for port in self.port:
            result = 1
            sys.stdout.flush()
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                r = sock.connect_ex((self.target, port))
                if r == 0:
                    result = r
                    sock.close()
            except Exception as e:
                pass
            if result == 0:
                self.port_ouvert.append(port)

class Network_scanner:
    def __init__(self, address_resau="192.168.100.0/24", interface="eth0"):
        self.target = address_resau
        self.interface = interface
        self.broadcastMac = "ff:ff:ff:ff:ff:ff"
        self.macList = []

    def scan_network(self):
        packet = Ether(dst=self.broadcastMac)/ARP(pdst=self.target)
        ans, _ = srp(packet, timeout=2, iface=self.interface, inter=0.1, verbose=False)
        self.macList = [(receive.psrc, receive.src) for _, receive in ans]

    def mac_table(self):
        print(tabulate(self.macList, headers=["Adresse IP", "Adresse MAC"], tablefmt="grid"))


choix = input("1.port scanner | 2.network scanner :")
if choix == 1:
    ip = input("adress reseaux (192.168.100.1/24) :")
    inter = input("interface :")
    n = Network_scanner(ip,inter)
    n.scan_network()
    n.mac_table()
else:
    ip = input("targe : ")
    p = Port_scanner(ip)
    p.scan_port()
    print(p.port_ouvert)
