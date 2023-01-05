import mysql.connector

import beneficiary
import transferFunds
import updateDetails
import registration

import main

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="1234",
    database="bank_info"
)
mycursor = mydb.cursor()


def checking_login_details(username, pin):
    """
    checks the login credentials entered are valid or not.
    :return: True if login credentials are correct else False.
    """
    cq_card_cvv = f'''
        SELECT balance
        FROM balance JOIN users
        ON balance.user_id = users.id
        WHERE users.username = '{username}' AND m_pin = {pin}
    '''
    mycursor.execute(cq_card_cvv)
    result = mycursor.fetchone()

    # if any login detail is incorrect value of result will be 'None'
    if not result:
        return False
    return True


def list_bank_details(username):
    """
    Returns the list of tuples containing information like username, account_number, mobile number, CVV and card type
    """
    query1 = f'''
            SELECT username, account_number, mobile_no, card_cvv, card_type
            FROM users JOIN cards
            ON users.id = cards.user_id
            WHERE username = "{username}"
        '''
    mycursor.execute(query1)
    result = mycursor.fetchall()
    return result


def list_card_cvvs(username):
    """
    Returns the list of all card CVVs owned by user.
    """
    query1 = f'''
        SELECT card_cvv
        FROM users JOIN cards
        ON users.id = cards.user_id
        WHERE username = "{username}"
    '''
    mycursor.execute(query1)
    result = mycursor.fetchall()

    ans = []
    for i in result:
        ans.append(i[0])
    return ans


def display_details(username):
    """
    Prints the user information corresponding to the username provided.
    Prints list of cards, list of beneficiaries, current balance, and username
    """
    cards = list_bank_details(username)

    print(f"Username: {cards[0][0]}")
    print(f"Account Number: {cards[0][1]}")

    query2 = f'''
        SELECT balance
        FROM balance JOIN users
        ON balance.user_id = users.id
        WHERE username = "{username}"
    '''
    mycursor.execute(query2)
    result1 = mycursor.fetchall()

    print(f"Current Balance: {result1[0][0]}")

    beneficiary.print_beneficiaries(username)

    print("\nDetails of your credit and debit cards: ")
    for i in range(len(cards)):
        print(f"{i + 1}. {cards[i][-1]} card CVV: {cards[i][-2]}")
    print("\n")


def update_details(username):
    """
    Update user's address, city, state and mobile number.
    Also checks validation of new entries provided by user.
    :param username:
    """
    print("\nYou choose to update your information.")
    print("Please Enter 1 to change your address.")
    print("Please Enter 2 to change your city.")
    print("Please Enter 3 to change your state.")
    print("Please Enter 4 to change your mobile number.")
    print("Please Enter 0 to exit.")

    t = int(input("Key: "))
    while t != 0:
        if t == 1:
            new_address = input("Please enter your new address: ")
            updateDetails.update_address(username, new_address)
            print("Address Updated")
        elif t == 2:
            new_city = input("Please enter your new city: ")
            while not registration.checking_city(new_city):
                print("Please enter a valid city")
                new_city = input("Please enter your new city: ")

            updateDetails.update_city(username, new_city)
            print("City Updated")
        elif t == 3:
            new_state = input("Please enter your new state: ")
            while not registration.checking_state(new_state):
                print("Please enter a valid state")
                new_state = input("Please enter your new state: ")

            updateDetails.update_state(username, new_state)
            print("State Updated")
        elif t == 4:
            new_mobile_no = input("Please enter your new mobile number without any spaces and any characters: ")
            while not registration.checking_mobile_no(new_mobile_no):
                print("Please enter a valid 10 digit mobile number")
                new_mobile_no = input("Please enter your new mobile number without any spaces and any characters: ")

            updateDetails.update_mobile_no(username, new_mobile_no)
            print("Mobile Number Updated")

        print("Please Enter 1 to change your address.")
        print("Please Enter 2 to change your city.")
        print("Please Enter 3 to change your state.")
        print("Please Enter 4 to change your mobile number.")
        print("Please Enter 0 to exit.")
        t = int(input("Key: "))

    print("Your information has been updated")
    login_functions(username)


def change_pin(username):
    """
    changes pin of the card.
    Also checks validation of the new pin entered by user.
    """
    print("You chose to change your pin")
    t = 1
    while t == 1:
        cvv = input("Please enter the cvv of the card whose Pin you want to change: ")
        while not registration.checks_cvv(cvv):
            print("Wrong CVV!!")
            cvv = input("Please enter the cvv of the card whose Pin you want to change: ")

        while cvv not in list_card_cvvs(username):
            print("No such card!!")
            cvv = input("Please enter the cvv of the card whose Pin you want to change: ")
            while not registration.checks_cvv(cvv):
                print("Wrong CVV!!")
                cvv = input("Please enter the cvv of the card whose Pin you want to change: ")

        pin = input("Please enter the pin of your card: ")
        while not registration.checks_valid_pin(pin):
            print("Please enter a valid 4 digit numeric pin")
            pin = input("Please enter the pin of your card: ")
        while not registration.checks_pin(username, cvv, pin):
            print("Wrong pin!!")
            pin = input("Please enter the pin of your card: ")
            while not registration.checks_valid_pin(pin):
                print("Please enter a valid 4 digit numeric pin")
                pin = input("Please enter the pin of your card: ")

        new_pin1 = input("Please enter new 4 digit pin: ")
        while not registration.checks_valid_pin(new_pin1):
            print("Please enter a valid 4 digit pin")
            new_pin1 = input("Please enter new 4 digit pin: ")
        confirm_pin = input("Please re-enter your new pin: ")
        while confirm_pin != new_pin1:
            print("Pin didn't match!!")
            new_pin1 = input("Please enter new 4 digit pin: ")
            while not registration.checks_valid_pin(new_pin1):
                print("Please enter a valid 4 digit pin")
                new_pin1 = input("Please enter new 4 digit pin: ")
            confirm_pin = input("Please re-enter your new pin: ")
        if new_pin1 == confirm_pin:
            updateDetails.change_pin(username, cvv, pin, new_pin1)
            print("PIN changed!!")
        t = int(input("To exit please enter 0 or to change pin of other card enter 1: "))

    login_functions(username)


def add_credit_card(username):
    print("Adding new Credit Card")
    pin = input("Please Enter the pin of your new credit card: ")
    while not registration.checks_valid_pin(pin):
        print("Please enter a valid 4 digit numeric pin")
        pin = input("Please enter the pin of your card: ")

    cvv = updateDetails.add_new_credit_card(username, pin)
    print("New credit card added")
    print(f"CVV of your new credit is {cvv}")

    t = input("Press 0 to exit: ")
    while not t.isnumeric() or len(t) != 1 or t != '0':
        t = input("Press 0 to exit: ")

    login_functions(username)


def add_beneficiary_2(username):
    """
    Checks validation of name and account number of the beneficiary
    Also checks if the beneficiary is present in the database or not
    After all validations insert the beneficiary into beneficiary table using add_beneficiary()
    function in beneficiary file.
    """
    print("Adding a beneficiary")
    b_name = input("Please Enter the name of the beneficiary: ")
    while not registration.checking_name(b_name):
        print("Invalid Name!")
        b_name = input("Please Enter the name of the beneficiary: ")

    b_account_number = input("Please enter beneficiary account number: ")
    while not registration.checks_account_number(b_account_number):
        print("Invalid Account Number")
        b_account_number = input("Please enter beneficiary account number: ")

    while not beneficiary.checks_beneficiary_and_account_no(b_name, b_account_number):
        print("Invalid name and account number")
        b_name = input("Please Enter the name of the beneficiary: ")
        while not registration.checking_name(b_name):
            print("Invalid Name!")
            b_name = input("Please Enter the name of the beneficiary: ")

        b_account_number = input("Please enter beneficiary account number: ")
        while not registration.checks_account_number(b_account_number):
            print("Invalid Account Number")
            b_account_number = input("Please enter beneficiary account number: ")

    beneficiary.add_beneficiary(username, b_name, b_account_number)
    print("Beneficiary Added")
    beneficiary.print_beneficiaries(username)

    t = input("Press 0 to exit: ")
    while not t.isnumeric() or len(t) != 1 or t != '0':
        t = input("Press 0 to exit: ")

    login_functions(username)


def transfer_money(username):
    """
    Transfer money to another account
    """
    transferFunds.take_user_information(username)
    t = input("Press 0 to exit: ")
    while not t.isnumeric() or len(t) != 1 or t != '0':
        t = input("Press 0 to exit: ")

    login_functions(username)


def change_mpin(username):
    """
    changes the mPIN of the account. Also checks the validation of new mPIN
    """
    print("Changing mPIN")
    c_mpin = input("Please enter your current mPIN")
    while not registration.check_mpin(c_mpin):
        print("Please enter a valid 6 digit numeric mPIN")
        c_mpin = input("Please enter your current mPIN")

    while not checking_login_details(username, c_mpin):
        print("Wrong mPIN!!!")
        c_mpin = input("Please enter your current mPIN: ")
        while not registration.check_mpin(c_mpin):
            print("Please enter a valid 6 digit numeric mPIN")
            c_mpin = input("Please enter your current mPIN: ")

    new_mpin = input("Please enter your new mPIN: ")
    while not registration.check_mpin(new_mpin):
        print("Please enter a valid 6 digit numeric mPIN")
        new_mpin = input("Please enter your new mPIN: ")

    confirm_mpin = input("Please re-enter your new mPIN: ")
    while confirm_mpin != new_mpin:
        print("PIN didn't match!!!")
        new_mpin = input("Please enter your new mPIN: ")
        while not registration.check_mpin(new_mpin):
            print("Please enter a valid 6 digit numeric mPIN")
            new_mpin = input("Please enter your new mPIN: ")

        confirm_mpin = input("Please re-enter your new mPIN: ")

    if confirm_mpin == new_mpin:
        updateDetails.change_mpin(username, new_mpin)
    print("Your mPIN has been changed")

    t = input("Press 0 to exit: ")
    while not t.isnumeric() or len(t) != 1 or t != '0':
        t = input("Press 0 to exit: ")

    login_functions(username)


def login_functions(username):
    """
    All login features once the user logins
    """
    print("\n\n")
    display_details(username)

    print("Press 1 to update your information")
    print("Press 2 to change your card's pin")
    print("Press 3 to apply for new credit card")
    print("Press 4 to add a beneficiary")
    print("Press 5 to transfer money")
    print("Press 6 to change you mPIN")
    print("Press 0 to logout")
    t = input("Key: ")
    while not t.isnumeric() or len(t) != 1:
        print("Please enter a valid key")
        t = input("Key: ")
    t = int(t)
    if t == 1:
        update_details(username)
    elif t == 2:
        change_pin(username)
    elif t == 3:
        add_credit_card(username)
    elif t == 4:
        add_beneficiary_2(username)
    elif t == 5:
        transfer_money(username)
    elif t == 6:
        change_mpin(username)
    elif t == 0:
        print("Logout Successful!!")
        main.home_page()


def login_menu():
    """
    Main login menu which asks for login details.
    If login credentials are correct user can update her/his address, city, state, mobile_number and
    pin of the cards available.
    """
    print("\nLogin into your Bank Account")
    username = input("Please enter your username: ")
    while not registration.checking_only_username(username):
        print("Please enter a valid username containing only alphabets and '_'")
        username = input("Please enter your username: ")

    mpin = input("Please enter your mPIN: ")
    while not registration.check_mpin(mpin):
        print("Please Enter a valid 6 digit numeric mPIN")
        mpin = input("Please enter your mPIN: ")

    r = checking_login_details(username, mpin)
    while not r:
        print("Wrong Login Credentials!!!\nPlease Login Again.")
        username = input("Please enter your username: ")
        while not registration.checking_only_username(username):
            print("Please enter a valid username containing only alphabets and '_'")
            username = input("Please enter your username: ")

        mpin = input("Please enter your mPIN: ")
        while not registration.check_mpin(mpin):
            print("Please Enter a valid 6 digit numeric mPIN")
            mpin = input("Please enter your mPIN: ")

        r = checking_login_details(username, mpin)

    print("Login Successful")
    login_functions(username)


def close_db():
    mycursor.close()
    mydb.close()
