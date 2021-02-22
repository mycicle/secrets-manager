import os
import sqlite3

from Crypt import Crypt
from KeyGen import KeyGen

def check_password(username, inp):
    return True
def delete_db_confirmation_loop(username: str) -> None:
    delete_db = input(f"Do you want to delete the existing user information for {username}? (yes/no) ").lower()
    while True:
        if delete_db == "yes":
            if check_password(username, input("Please input that user's password: ")):
                os.remove(f"{username}.db")
                print(f"User information for {username} deleted")
                return
            else:
                print("Incorrect password, no information has been removed")
                exit()

        elif delete_db == "no":
            print("No information has been removed")
            return

        else:
            print("Please input either 'yes' or 'no'")

def initialize_new_user() -> None:
    username: str = input("Please input your username, no special characters, backslashes (\\) or spaces:")
    key_generator = KeyGen()
    key, salt = key_generator.generate_new(input("Please input your user password for initialization: "))
    # salt_key_str = ":".join(key.dec)
    if os.path.exists(f"{username}.db"):
        # delete_db_confirmation_loop(username)
        pass

    conn = sqlite3.connect(f"{username}.db")
    c = conn.cursor()
    c.execute(
        """
            CREATE TABLE accounts
            (application text, password text, mnemonic text, pin text, additional text)
        """
    )
    c.execute(
        """
            INSERT INTO accounts (password) VALUES
            (?)
        """,
        (key.hex() + salt.hex(), )
    )
    conn.commit()
    conn.close()
    
def main():

    conn = sqlite3.connect(f"{input('username: ')}.db")
    c = conn.cursor()

    c.execute(
        """
            SELECT * FROM accounts
        """
    )
    row = c.fetchone()
    if (row is None):
        print("No valid database entry for input")
        
    password_bytes = bytes.fromhex(row[1])
    loaded_key = password_bytes[:-32]
    loaded_salt = password_bytes[-32:]

    key_generator = KeyGen()
    check_key = key_generator.from_existing(input("Please input your password"), loaded_salt)

    if check_key != loaded_key:
        print("bad password")

    crypt = Crypt(check_key)

    message_to_encrypt = "Message 1234$%^"
    print(message_to_encrypt)
    print(crypt.encrypt(message_to_encrypt))
    print(crypt.decrypt(crypt.encrypt(message_to_encrypt)))

if __name__ == "__main__":
    initialize_new_user()
    main()