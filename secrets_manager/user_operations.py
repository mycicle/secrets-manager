import re
import sqlite3
from os.path import join

from KeyGen import KeyGen
from UserData import UserData
from constants import base_keypath, base_datapath, keypaths

def create_user(username: str):
    """
    Generate a new key and salt combination for a new user
    Generate a database with an empty table for that user
    Save the key, salt combination to disk
    """
    print("You are about to input the password used to encrypt all of your data. Make it strong and write it down")
    print("Nobody will be able to recover your password or your data if you forget it.")
    print("You will be able to recover your private key from your password and a ranomly generated number called 'salt'")
    print(
        """
        To make your data more resistant to brute force attacks, we add
        'salt' to your password. Salt is a random sequence of numbers that can be used
        to obscure your true password. You will have to write down your 'salt' as well as your password
        If you want to recover your private key you will need to input your 'salt' as well.
        """
    )
    password: str = str(input("Please input your new user password for initialization: "))
    while True:
        check_password = input(f"Your password is: {password}\nEnter your password to confirm that you have it copied down correctly:\n  ")
        if check_password == password:
            print("Correct")
            break
        else:
            print(f"Incorrect, the correct password is: \n{password}")
            continue

    key_generator: KeyGen = KeyGen()
    key, salt = key_generator.generate_new(password)
    print(f"Your salt is: {salt.hex()}")

    while True:
        check_salt = input(f"Your salt value is: {salt.hex()}\nEnter your salt value to confirm that you have it copied down correctly:\n  ")
        if check_salt == salt.hex():
            print("Correct")
            break
        else:
            print(f"Incorrect, the correct salt value is: \n{salt.hex()}")
            continue

    _ = input("Press 'enter' to continue once you have written down your salt and your password.\nTHIS IS THE LAST TIME YOU WILL BE ABLE TO SEE THEM")

    private_keypath: str = join(base_keypath, '.'.join([username, 'key']))
    print(f"saving private key to: {private_keypath}")

    user_datapath: str = join(base_datapath, '.'.join([username, 'db']))
    print(f"saving user data to: {user_datapath}")

    key_salt_str: str = key.hex() + salt.hex()
    with open(private_keypath, 'w') as file:
        file.write(key_salt_str)
    
    conn = sqlite3.connect(user_datapath)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE accounts
        (application text, password text, mnemonic text, pin text, additional text)
        """
    )
    conn.commit()
    conn.close()
    keypaths[username] = UserData(private_keypath, user_datapath)

