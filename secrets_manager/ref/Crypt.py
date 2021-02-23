import base64
from cryptography.fernet import Fernet

from typing import Union

class Crypt:
    def __init__(self, key: bytes):
        self.f = Fernet(key)

    def encrypt(self, information: Union[bytes, str]) -> bytes:
        if not isinstance(information, (str, bytes)):
            raise TypeError("Invalid information type")

        if isinstance(information, str):
            information = information.encode()
        
        return self.f.encrypt(information)

    def decrypt(self, information: bytes) -> str:
        return self.f.decrypt(information).decode()