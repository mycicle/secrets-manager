import argparse
import sqlite3
import base64
import os
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def main():

    hasher = hashlib.sha256()
    hasher.update(input("Input your password ").encode()) # this is a bytes object
    cpass = hasher.digest()

    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(
        """
            SELECT * FROM accounts
        """
        # ('algorand_wallet',)
    )
    row = c.fetchone()
    if (row is None):
        print("No valid database entry for input")
    print(row)

    salt: bytes = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )

    key = base64.b64encode(kdf.derive(cpass))

    f = Fernet(key)
    encrypted = f.encrypt(input("Message to encrypt").encode())
    print(encrypted)

    decrypted = f.decrypt(encrypted)
    print(decrypted)






if __name__ == "__main__":
    password = "asdf"
    hasher = hashlib.sha256()
    hasher.update(password.encode())
    hashpass = hasher.digest().hex()

    wallet_name = "algorand wallet"
    seed_phrase = ["Hello", "how", "are", "you", "doing"]
    mnemonic = ':'.join(seed_phrase)

    pin = "123456"

    additional = "Some other additional string information https://google.com heres a link"
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    # c.execute(
    #     '''
    #         CREATE TABLE accounts
    #         (application text, password text, mnemonic text, pin text, additional text)
    #     '''
    # )
    c.execute(
        """
            INSERT INTO accounts(application, password, mnemonic, pin, additional) VALUES
            (?, ?, ?, ?, ?);
        """,
        (wallet_name, hashpass, mnemonic, pin, additional)
    )
    conn.commit()
    conn.close()
    main() 