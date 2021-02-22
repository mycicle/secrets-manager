
from constants import keypaths
from user_operations import create_user
def new_user():
    print(keypaths)
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
                login()
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
                    delete_user()
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

def returning_user():
    print(keypaths)

def login():
    print(keypaths)

def delete_user():
    _delete_data: int = int(input(
        f"""
        Do you want to delete user {username}'s data?
        1. Yes
        2. No
        """
    ))