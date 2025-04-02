import sys
import socket

from tabulate import tabulate # pour affichage self.macList
# python -m pip install tabulate
from scapy.all import Ether, ARP, srp
# apt install python3-scapy
# python -m pip install scapy

class Port_scanner :
    def __init__(self,ip):
        self.target = ip
        self.port = range(1,65535)
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

class Network_scanner :
    def __init__(self,address_resau = "192.168.X.X/24",interface = "eth0"):
        self.target = address_resau
        self.interface = interface
        self.broadcastMac = "ff:ff:ff:ff:ff:ff"
        self.macList = []
    
    def scan_network(self):
        packet = Ether(dst=self.broadcastMac)/ARP(pdst=self.target)
        ans, _ = srp(packet, timeout=2, iface=self.interface, inter=0.1, verbose=False)
        self.macList = [(receive.psrc, receive.src) for _, receive in ans]
        
        # print(tabulate(results, headers=["Adresse IP", "Adresse MAC"], tablefmt="grid"))        

# n = Network_scanner("10.10.10.10","m")
# print(n.target,n.interface)
    

# target = Port_scanner("10.10.53.128")
# target.port_scan()
# print(target.port_ouvert)