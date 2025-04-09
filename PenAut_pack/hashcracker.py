import hashlib
import os

class NoSaltedHashCracker:
    def __init__(self, algo, wordlist_path, hash_value):
        self.algorithm = algo.lower()
        self.wordlist_path = wordlist_path
        self.target_hash = hash_value

    def cracking(self):
        if self.algorithm not in ['md5', 'sha1', 'sha256', 'sha512', 'sha224', 'sha384']:
            print(f"❌ Error: '{self.algorithm}' is not a supported hash algorithm.")
            return

        if not os.path.isfile(self.wordlist_path):
            print(f"❌ Error: Wordlist file '{self.wordlist_path}' was not found.")
            return

        with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                word = line.strip()
                hashed = getattr(hashlib, self.algorithm)(word.encode()).hexdigest()
                if hashed == self.target_hash:
                    print(f"✅ Password found: {word}")
                    return
        print("❌ Password not found in the wordlist.")

def main_hashcracker():
    algo = input("Which algorithm? [md5, sha1, sha256, sha512, sha224, sha384]: ").strip().lower()
    hash_value = input("Enter the hash to crack: ").strip()
    wordlist_path = input("Wordlist path? (Press Enter for default: /usr/share/wordlists/rockyou.txt): ").strip()

    if not wordlist_path:
        wordlist_path = "/usr/share/wordlists/rockyou.txt"

    cracker = NoSaltedHashCracker(algo, wordlist_path, hash_value)
    cracker.cracking()
