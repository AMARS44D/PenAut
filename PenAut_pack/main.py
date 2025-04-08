import os,sys
from PenAut_pack.cve_scan import main_scancve
from cve_search import main_cve
from hashcracker import NoSaltedHashCracker,main_hashcracker
from network_scanner import Network_scanner,main_net
from passpwnd import CheckPasswordPwned,main_passpwnd
from port_scanner import main_port
from shodan_scan import main_shodan
from url_enum import WordlistLoader,DomainScanner,main_url_enum
from tool_style import banner,clear



#Vérification des droits root
if os.geteuid() != 0:
    print("❌ Ce script doit être exécuté en root (utilisez sudo).")
    sys.exit(1)

choice=10
while choice !=0 : 
    choice=10
    clear()
    banner()
    print("\n\n------> TAP 0 TO QUIT <------\n\n")
    print(" 1 - Network Scanner               :")
    print(" 2 - port scanner                  :")
    print(" 3 - Shodan Scan                   :")
    print(" 4 - Url Enumeration               :")
    print(" 5 - CVE Search                    :")
    print(" 6 - CVE Scan                      :")
    print(" 7 - Hash Cracker                  :")
    print(" 8 - Password Pwned                ?")
    choice=int(input("------------------------------------>  "))

    var=1
    if choice==1 : 
        while var != 0 :  
            main_net()
            var=int(input("------> TAP 0 TO QUIT <------"))
            clear()
            banner()
    elif choice == 2 : 
        while var !=0 : 
            main_port()
            var=int(input("------> TAP 0 TO QUIT <------"))
            clear()
            banner()
    elif choice == 3 :
        while var != 0 :  
            main_shodan()        
            var=int(input("------> TAP 0 TO QUIT <------"))
            clear()
            banner() 

    elif choice == 4 : 
        while var != 0 : 
            main_url_enum()
            var=int(input("------> TAP 0 TO QUIT <------"))
            clear()
            banner()
    elif choice == 5 :
            while var != 0 : 
                main_cve()
                var=int(input("------> TAP 0 TO QUIT <------"))
                clear()
                banner()
    elif choice == 6 : 
        while var != 0 :
            main_scancve()
            var=int(input("------> TAP 0 TO QUIT <------"))
            clear()
            banner()
    elif choice == 7 : 
        while var != 0 :
            main_hashcracker()
            var=int(input("------> TAP 0 TO QUIT <------"))
            clear()
            banner() 
    elif choice == 8 : 
        while var != 0 :   
            main_passpwnd()
            var=int(input("------> TAP 0 TO QUIT <------"))
            clear()
            banner()

