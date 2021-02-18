import argparse
import sqlite3
import base64
import os
import hashlib

def main():

    inpass = input("Input your password ").encode('utf-8')

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
        raise RuntimeError("No valid database entry for input")

    salt = row[1][:32]
    key = row[1][32:]

    checked_key = hashlib.pbkdf2_hmac(
        'sha256',
        inpass,
        salt, 
        100000
    )

    if (key != checked_key):
        print("Invalid password")
        print(f"key: {key}")
        print(f"checked_key: {checked_key}")
        print(f"salt: {salt}")
    else:
        print("yay, they matched")
        print(f"key: {key}")
        print(f"checked_key: {checked_key}")
        print(f"salt: {salt}")

    






if __name__ == "__main__":
    password = "asdf"
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,
    )
    print(f"key: {key}")
    print(f"salt: {salt}")
    hashpass = salt + key
    wallet_name = "algorand wallet"
    seed_phrase = ["Hello", "how", "are", "you", "doing"]
    mnemonic = ':'.join(seed_phrase)

    pin = "123456"

    additional = "Some other additional string information https://google.com heres a link"
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute(
        '''
            CREATE TABLE accounts
            (application text, password text, mnemonic text, pin text, additional text)
        '''
    )
    c.execute(
        """
            INSERT INTO accounts (application, password, mnemonic, pin, additional) VALUES
            (?, ?, ?, ?, ?);
        """,
        (wallet_name, hashpass, mnemonic, pin, additional)
    )
    conn.commit()
    
    main()
    c.execute(
        """
            DROP TABLE accounts
        """
    )
    conn.commit()
    conn.close()
    