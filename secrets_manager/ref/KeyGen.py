import os
import re
import base64
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from typing import Tuple
class KeyGen:
    def __init__(self):
        pass
    
    def generate_new(self, password: str) -> Tuple[bytes, bytes]:
        validated_password = self.validate_password_format(password)
        hashed_password: bytes = self.hash_password(validated_password)
        salt = os.urandom(32)

        key = self._get_key(hashed_password, salt)

        return (key, salt)

    def from_existing(self, password: str, salt: bytes) -> bytes:
        hashed_password: bytes = self.hash_password(password)
        key = self._get_key(hashed_password, salt)

        return key

    def validate_password_format(self, password: str) -> str:
        while True:
            proper_format = self.check_format(password)
            if not proper_format:
                print("Please use a different password")
                password = input("Enter a new password: ")
                continue
            else:
                break

        self.confirm(password)

        return password

    def hash_password(self, password: str) -> bytes:
        hasher = hashlib.sha256()
        hasher.update(password.encode())
        hashed_password = hasher.digest()

        return hashed_password

    def check_format(self, password: str) -> bool:
        regex = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{8,}$')
        result = re.match(regex, password)

        if result:
            print("Nice password")
            return True
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
            return False
    
    def confirm(self, password):

        correct = False
        while not correct:
            check = input("Please re enter your password: ")
            print(password == check)
            if password != check:
                continue
            else: 
                correct = True
                break
        
        print("Password input correctly, make sure you remember it!")
        print("If you lose it NOBODY can recover your data")

    @staticmethod
    def _get_key(hashed_password: bytes, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(hashed_password))

        return key
