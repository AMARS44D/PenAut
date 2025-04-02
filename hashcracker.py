import hashlib

class NoSaltedHashCracker:
    def __init__(self, algo, wlp, hash):
        self.algorithme = algo
        self.wordlistpath = wlp
        self.hash = hash
    
    def cracking(self):
        if self.algorithme not in ['md5', 'sha1', 'sha256', 'sha512', 'sha224', 'sha384']:
            print(f"Error: {self.algorithme} is not a supported hash type.")
            return
        
        with open(self.wordlistpath, 'r') as file:
            for line in file.readlines():
                if self.algorithme == 'md5':
                    hash_ob = hashlib.md5(line.strip().encode())
                elif self.algorithme == 'sha1':
                    hash_ob = hashlib.sha1(line.strip().encode())
                elif self.algorithme == 'sha256':
                    hash_ob = hashlib.sha256(line.strip().encode())
                elif self.algorithme == 'sha224':
                    hash_ob = hashlib.sha224(line.strip().encode())
                elif self.algorithme == 'sha512':
                    hash_ob = hashlib.sha512(line.strip().encode())
                elif self.algorithme == 'sha384':
                    hash_ob = hashlib.sha384(line.strip().encode())
                else:
                    print(f"Error: {self.algorithme} is not a supported hash type.")
                    return
                
                hashed_pass = hash_ob.hexdigest()
                if hashed_pass == self.hash:
                    print('Found cleartext password! ' + line.strip())
                    return
        
        print("Password not found in the wordlist.")

hh = NoSaltedHashCracker('md5', 'wl.txt', '3ab896b5b94e97beb42b6d91294dbd62')
hh.cracking()
