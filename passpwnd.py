import hashlib
import requests

class CheckPasswordPwned:
    def __init__(self, passwd):
        self.password = passwd

    def check(self):
        sha1 = hashlib.sha1(self.password.encode('utf-8')).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)

        if response.status_code == 200:
            hashes = response.text.splitlines()
            found = any(suffix in line for line in hashes)
            if found:
                print("⚠️ Ce mot de passe a été compromis !")
            else:
                print("✅ Ce mot de passe ne figure pas dans les fuites connues.")
        else:
            print(f"Erreur {response.status_code} : {response.text}")

def main_passpwnd() : 
    pass1=input("Enter the password to check : ")
    password=CheckPasswordPwned(pass1)
    password.check()