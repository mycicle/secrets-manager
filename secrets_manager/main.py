from states import new_user, returning_user
from enums import UserType
from constants import keypaths

def main():
    """
    main function to simulate the different states of the appilcation
    this will use simple if statements to move from state to state, the focus
    for now is on the primary application logic and the encryption, not the UI
    initially some checks will be bypassed for ease of debugging
    """

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
            break
        elif _user_type == 2:
            returning_user()
            break
        elif _user_type == 3:
            print("Goodbye")
            break
        else:
            print("Invalid choice, please try again")
            continue
        


if __name__ == "__main__":
    main()