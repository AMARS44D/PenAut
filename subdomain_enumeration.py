import requests  # type: ignore
from concurrent.futures import ThreadPoolExecutor

class WordlistLoader:
    @staticmethod
    def load(filename):
        try:
            with open(filename, "r", encoding="utf-8", errors="ignore") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print(f"Erreur: Le fichier '{filename}' est introuvable.")
            return []

class DomainScanner:
    def __init__(self, domain, choice="1"):
        self.domain = domain
        self.subdomains_file = ""
        self.directories_file = ""
        self.choice = choice
        self.extensions = ["", ".txt", ".php", ".html", ".zip", ".rar", ".htm", ".asp", ".aspx", ".jsp"]
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        self.urls = []

    def prepare_urls(self):
        if self.choice in ["1", "3"]:
            self.subdomains_file = input("Wordlist pour subdomains (rockyou.txt par défaut) : ") or "/usr/share/wordlists/rockyou.txt"
            subdomains = WordlistLoader.load(self.subdomains_file)
            self.urls.extend([f"http://{sub}.{self.domain}" for sub in subdomains])
        
        if self.choice in ["2", "3"]:
            self.directories_file = input("Wordlist pour directories et fichiers (rockyou.txt par défaut) : ") or "/usr/share/wordlists/rockyou.txt"
            directories = WordlistLoader.load(self.directories_file)
            for directory in directories:
                for ext in self.extensions:
                    self.urls.append(f"http://{self.domain}/{directory}{ext}")

    def check_url(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                print(f"[+] Valide: {url}")
        except requests.RequestException:
            pass  # Ignorer les erreurs

    def run_scan(self):
        print(f"\n🔍 Scanning {self.domain}...\n")
        self.prepare_urls()
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.check_url, self.urls)
        print("\n✅ Scan terminé.")

if __name__ == "__main__":
    domain = input("Domaine : ")
    print("\nQue voulez-vous scanner ?")
    print("1. Sous-domaines")
    print("2. Sous-répertoires et fichiers")
    print("3. Les deux")
    choice = input("Entrez votre choix (1/2/3) : ")

    
    
    
    scanner = DomainScanner(domain, choice)
    scanner.run_scan()
