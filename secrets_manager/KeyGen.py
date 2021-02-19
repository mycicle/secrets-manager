import os
import re
import base64
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class KeyGen:
    def __init__(self, password: str):
        self.check_format(password)
        self.confirm(password)

        hasher = hashlib.sha256()
        hasher.update(password.encode())
        self.hashed_password = hasher.digest()

        self.salt = os.urandom(32)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )

        self.key = base64.urlsafe_b64encode(kdf.derive(self.hashed_password))
    
    def check_format(self, password: str) -> None:
        regex = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{8,}$')
        result = re.match(regex, password)

        if result:
            print("Nice password")
        else:
            print(
                """
                    Password requirements: 

                    Should contain at least one capital letter
                    Should contain at least one lower case letter
                    Should contain at least one number
                    Should contain at least one special character
                    Should be longer than 8 characters
                """
            )
            raise ValueError("Bad password")
    
    def confirm(self, password):

        correct = False
        while not correct:
            check = input("Please re enter your password: ")
            if password != check:
                continue
            else: 
                correct = True
                break
        
        print("Password inputted correctly twice, make sure you remember it!")
        print("If you lose it NOBODY can recover your data")


