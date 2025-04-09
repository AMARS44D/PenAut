import requests  # type: ignore
from concurrent.futures import ThreadPoolExecutor


class WordlistLoader:
    @staticmethod
    def load(filename):
        try:
            with open(filename, "r", encoding="utf-8", errors="ignore") as file:
                return [
                    line.strip()
                    for line in file
                    if line.strip() and not line.lstrip().startswith("#")
                ]
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
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
            self.subdomains_file = input("Wordlist for subdomains (/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt by default 'ENTER'):") or "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"
            subdomains = WordlistLoader.load(self.subdomains_file)
            self.urls.extend([f"http://{sub}.{self.domain}" for sub in subdomains])
        
        if self.choice in ["2", "3"]:
            self.directories_file = input("Wordlist for directories and files (/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt by default 'ENTER'):") or "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"
            directories = WordlistLoader.load(self.directories_file)
            for directory in directories:
                for ext in self.extensions:
                    self.urls.append(f"http://{self.domain}/{directory}{ext}")

    def check_url(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                print(f"[+] Valid: {url}")
        except requests.RequestException:
            pass  # Ignorer les erreurs

    def run_scan(self):
        print(f"\n🔍 Scanning {self.domain}...\n")
        self.prepare_urls()
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.check_url, self.urls)
        print("\n✅ Scan terminé.")

def main_url_enum() : 
    domain = input("Enter a domain : ")
    print("\nWhat do you want to scan?")
    print("1. Sub-domains")
    print("2. Directory and files ")
    print("3. Both")
    choice = input("Choose one (1/2/3) : ")
    scanner = DomainScanner(domain, choice)
    scanner.run_scan()
