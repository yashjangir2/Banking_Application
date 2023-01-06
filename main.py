import creatingDB
import login
import registration
import updateDetails
import transferFunds
import beneficiary


def encryption_pass():
    """
    Set you encryption and decryption password for PINs
    """
    return 'pass'


def home_page():
    """
    Options for login, register or exit.
    Closes all the mySQL servers after exiting
    """
    print("Hello! Welcome to XYZ Bank")
    print("Press 1 to login")
    print("press 2 to register")
    print("press 0 to exit")
    key = input("Key: ")
    while not key.isnumeric() or len(key) != 1 or int(key) < 0 or int(key) > 2:
        print("Invalid key!!!")
        key = input("Key: ")
    key = int(key)

    if key == 1:
        login.login_menu()
    elif key == 2:
        print("\nRegistering New User")
        registration.registering_user()
    elif key == 0:
        updateDetails.close_db()
        registration.close_db()
        login.close_db()
        transferFunds.close_db()
        beneficiary.close_db()
        creatingDB.close_db()
        print("Thank you!!!")


if __name__ == "__main__":
    creatingDB.creating_all_tables()
    home_page()
