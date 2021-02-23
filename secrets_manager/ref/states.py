import os
import sqlite3

from Crypt import Crypt
from KeyGen import KeyGen
from UserData import UserData
from user_operations import create_user
from constants import keypaths


def main_menu():
    while True:
        _user_type: int = int(input(
            """
            1. Do you want to make a new account
            2. Returning user
            3. Close
            """
        ))

        if _user_type == 1:
            new_user()
        elif _user_type == 2:
            returning_user()
        elif _user_type == 3:
            print("Goodbye")
            break
        else:
            print("Invalid choice, please try again")
            continue

def new_user():
    while True:
        username: str = str(input(
            """
            Input your new username:\n 
            """
        ))
        if username is None:
            print("Invalid username provided")
            continue
        if keypaths.get(username, None) is not None:
            print("That username has data associated with it")
            _login: int = int(input(
                f"""
                Do you want to login as user {username}?
                1. Yes
                2. No
                """
            ))
            if _login == 1:
                returning_user(username)
                break
            elif _login == 2:
                _delete_user: int = int(input(
                    f"""
                    Do you want to delete user {username} or create a different user?
                    1. Different User
                    2. Delete user {username}
                    """
                ))
                if _delete_user == 1:
                    continue
                elif _delete_user == 2:
                    delete_user(username)
                    break
                else:
                    print("Invalid choice")
                    continue
            else: 
                print("Invalid choice")
                continue
        else:
            create_user(username)
            break

def returning_user(username: str = None):
    if username is None:
        (successful, key, username) = login(input("Input your username: "))
    else:
        (successful, key, username) = login(username)

    if not successful:
        raise RuntimeError("An error was encountered during login")

    while True:
        _read_or_write: int = int(input(
            """
            Would you like to: 
            1. View your existing account information
            2. Add new account information
            3. Both
            """
        ))
        if _read_or_write == 1:
            read_info(key, username)
            break
        elif _read_or_write == 2:
            write_info(key, username)
            break
        elif _read_or_write == 3:
            read_and_write_info(key, username)
            break
        else:
            print("Invalid choice")
            continue

    return 

def login(username: str):
    successful: bool = False

    if username not in keypaths.keys():
        print("Username not found")
        main_menu()
        return (successful, None, username)

    key_salt_bytes: bytes = None
    with open(keypaths.get(username, None).keypath, 'r') as file:
        key_salt_bytes = bytes.fromhex(file.read())
    if key_salt_bytes is None:
        raise ValueError("Unable to read key for user")

    loaded_key: bytes = key_salt_bytes[:-32]
    loaded_salt: bytes = key_salt_bytes[-32:]


    key_generator: KeyGen = KeyGen()
    while True:
        check_key = key_generator.from_existing(input(f"Please input password for user {username}: "), loaded_salt)

        if check_key != loaded_key:
            print("Bad password")
            continue
        else:
            print("Successful login")
            successful = True
            break
    
    return (successful, check_key, username)

def delete_user(username: str):
    while True:
        _delete_data: int = int(input(
            f"""
            Do you want to delete user {username}'s data?
            1. Yes
            2. No
            """
        ))

        if _delete_data == 1:
            (successful, _, _) = login(username)
            if not successful:
                print("Invalid password")
                continue
            else:
                _confirmation: str = str(input(
                    f"""
                    ARE YOU SURE YOU WANT TO PERMANENTLY DELETE ALL OF USER {username}'s DATA?
                    (yes/no)
                    """
                )).lower()
                if _confirmation == "yes":
                    print(f"Removing all data associated with user {username}")
                    os.remove(keypaths.get(username, None).keypath)
                    os.remove(keypaths.get(username, None).datapath)
                    _ = keypaths.pop(username, None)
                    print(f"User {username}'s data has been permanently deleted")
                    return
                else:
                    continue
        else:
            break 
    
    return 
        

def read_info(key: bytes, username: str):
    conn = sqlite3.connect(keypaths.get(username, None).datapath)
    c = conn.cursor()
    
    c.execute(
        """
        SELECT * FROM accounts
        """
    )
    rows = c.fetchall()
    if rows is None:
        print("Error reading database")
        return
    elif rows == []:
        print("Database empty")
        return 
    else:
        crypt: Crypt = Crypt(key)
        fields: Tuple[str] = (
            "application",
            "password",
            "mnemonic",
            "pin",
            "additional information"
        )
        for row in rows:
            for field, item in zip(fields, row):
                print(f"{field}: {crypt.decrypt(item)}")
            print()

    conn.close()

    return

def write_info(key: bytes, username: str):
    conn = sqlite3.connect(keypaths.get(username, None).datapath)
    c = conn.cursor()

    application: str = str(input(
        """
        Please input the name of the application you are storing information for: 
        (Enter nothing or any placeholder text you want if this field is not pertinent) 
        """
    ))

    application_password: str = str(input(
        """
        Please input application's password:
        (Enter nothing or any placeholder text you want if this field is not pertinent) 
        """
    ))

    mnemonic: str = str(input(
        """
        Please input application's mnemonic:
        (Enter nothing or any placeholder text you want if this field is not pertinent) 
        (Enter the mnemonic separated by commas without pressing enter, like so: hello, how, are, you)
        Press enter only when you are done entering the mnemonic
        """
    ))

    pin: str = str(input(
        """
        Please input application's pin number:
        (Enter nothing or any placeholder text you want if this field is not pertinent) 
        (Enter the pin separated by commas without pressing enter, like so: 1, 2, 3, 4, 5)
        Press enter only when you are done entering the pin
        """
    ))

    additional: str = str(input(
        """
        Please input any additional information about the application you may need:
        (Enter one continuous string like with the pin or mnemonic, you can input any text you like)
        Please press enter only when you are done entering the additional information
        """
    ))

    crypt: Crypt = Crypt(key)
    c.execute(
        """
        INSERT INTO accounts (application, password, mnemonic, pin, additional) VALUES
        (?, ?, ?, ?, ?)
        """,
        (crypt.encrypt(application), 
         crypt.encrypt(application_password), 
         crypt.encrypt(mnemonic), 
         crypt.encrypt(pin), 
         crypt.encrypt(additional))
    )

    conn.commit()
    conn.close()
    print("Information Successfully Stored!")

def read_and_write_info(key: bytes, username: str):
    read_info(key, username)
    write_info(key, username)
