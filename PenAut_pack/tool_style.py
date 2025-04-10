import os 


def banner() : 
    print("""
                            ______                ___          _   
                            | ___ \              / _ \        | |  
                            | |_/ /  ___  _ __  / /_\ \ _   _ | |_ 
                            |  __/  / _ \| '_ \ |  _  || | | || __|    
                            | |    |  __/| | | || | | || |_| || |_ 
                            \_|     \___||_| |_|\_| |_/ \__,_| \__|  
                                        
        Automated Penetration Testing Toolkit for Fast and Efficient Security Audits.  
    Created By : Aourik Anas - Amar Saad - Bennani Yahya - Amsou Ismail - Laamri Sayf-Eddine                                        
                                            
""")
    
    
def clear() : 
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for macOS/Linux
        os.system('clear')
    banner()
