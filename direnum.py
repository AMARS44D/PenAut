#like gobuster easy
import requests

class SubdomainScanner:
    def __init__(self, domain_name, subdomain_file="subdomains.txt"):
        self.domain_name = domain_name
        self.subdomain_file = subdomain_file
    
    def load_subdomains(self):
        with open(self.subdomain_file, "r") as file:
            return file.read().splitlines()
    
    def scan(self):
        subdomains = self.load_subdomains()
        
        for sub in subdomains:
            url = f"http://{sub}.{self.domain_name}"
            
            try:
                requests.get(url)
            except requests.ConnectionError:
                pass
            else:
                print("Valid domain:", url)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    scanner = SubdomainScanner(domain)
    scanner.scan()
