from random import randint
import mysql.connector
from getpass import getpass
import login
from pwinput import pwinput

# connecting to sql server
mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="1234",
    database="bank_info"
)
mycursor = mydb.cursor()


def checking_name(name):
    """
    Checks that name contains only alphabets
    """
    if not name.replace(" ", "").isalpha() or len(name) > 100:
        return False
    return True


def checking_only_username(username):
    """
    Checks that username contains only contains alphabets and "_".
    """
    if not username.replace("_", "").isalpha() or len(username) > 150:
        return False
    return True


def checking_username(username):
    """
    checks if the username already exists in the table or not
    """
    if checking_only_username(username):
        try:
            query = f"SELECT * FROM users WHERE username = '{username}'"
            mycursor.execute(query)
            result = mycursor.fetchall()
            if len(result) != 0:
                print("Username already in use please use different username")
                return False
            else:
                return True
        except mysql.connector.errors.ProgrammingError:
            return True
    return False


def checking_city(city):
    """
    Checks city is valid i.e., only contains alphabets
    :param city:
    """
    if not city.replace(" ", "").isalpha():
        return False
    return True


def checking_state(state):
    """
    Checks that the state contains only alphabets
    :param state:
    """
    if not state.replace(" ", "").isalpha():
        return False
    return True


def checking_aadhaar(aadhaar):
    """
    Checks that aadhaar contains only contains numerics and length is 12 characters.
    """
    if not aadhaar.isnumeric() or len(aadhaar) != 12:
        return False
    return True


def checking_mobile_no(mobile_no):
    """
    Checks that mobile number contains only contains numerics and length is 10 characters.
    Also checks mobile number is registered in India
    """
    if not mobile_no.isnumeric() or len(mobile_no) != 10 or int(mobile_no) < 6200000000:
        return False
    return True


def checks_cvv(cvv):
    """
    checks the validation of cvv
    :param: cvv: should be string
    """
    if not cvv.isnumeric() or len(cvv) != 3:
        return False
    return True


def checks_cvv_for_user(username, cvv):
    """
    Checks that card with the given cvv is owned by user or not
    :return: True if cvv is correct and False otherwise
    """
    query = f'''
       SELECT username, account_number
       FROM users JOIN cards
       ON users.id = cards.user_id
       WHERE username = "{username}" AND CAST(AES_DECRYPT(card_cvv, 'pass') AS CHAR) = '{cvv}'
    '''
    mycursor.execute(query)
    result = mycursor.fetchall()

    if len(result) == 0:
        return False
    return True


def checks_valid_pin(pin):
    """
    checks pin is of 4 digit and is numeric
    :param: pin: should be string
    """
    if not pin.isnumeric() or len(pin) != 4:
        return False
    return True


def checks_pin(username, cvv, pin):
    """
    Checks if user entered correct pin for the card of corresponding cvv
    :return: True if pin is correct else returns False
    """
    query = f'''
       SELECT username, account_number
       FROM users JOIN cards
       ON users.id = cards.user_id
       WHERE username = "{username}" 
       AND CAST(AES_DECRYPT(card_cvv, 'pass') AS CHAR) = '{cvv}' 
       AND CAST(AES_DECRYPT(card_pin, 'pass') AS CHAR) = '{pin}'
    '''
    mycursor.execute(query)
    result = mycursor.fetchall()

    if len(result) == 0:
        return False
    return True


def checks_account_number(account_number):
    """
    Checks validation of account number
    """
    if not account_number.isnumeric() or len(account_number) != 12:
        return False
    return True


def check_mpin(mpin):
    """
    Checks validation of mPIN
    :param: mpin: should be string
    """
    if not mpin.isnumeric() or len(mpin) != 6:
        return False
    return True


def registration_form():
    """
    Takes user input and checks validation of all information provided.
    :return: Dictionary containing user information if all the information are valid.
    """
    name = input("Please Enter your name: ")
    while not checking_name(name):
        print("Please enter a valid name.")
        name = input("Please Enter your name: ")

    username = input("Please create a username without spaces and only using alphabets or '_'': ")
    while not checking_username(username):
        print("Please enter a valid username with only alphabets and '_'")
        username = input("Please create a username without spaces and only using alphabets or '_'': ")

    address = input("Please enter your permanent address: ")

    city = input("Please enter your city: ")
    while not checking_city(city):
        print("Please enter a valid city name")
        city = input("Please enter your city: ")

    state = input("Please enter your state: ")
    while not checking_state(state):
        print("Please enter a valid state")
        state = input("Please enter your state: ")

    aadhaar = input("Please enter your aadhaar number without any spaces or any characters: ")
    while not checking_aadhaar(aadhaar):
        print("Please enter a valid 12 digit Aadhaar Number")
        aadhaar = input("Please enter your aadhaar number without any spaces or any characters: ")

    mobile_no = input("Please enter your mobile number without any spaces or any characters: ")
    while not checking_mobile_no(mobile_no):
        print("Please enter a valid 10 digit Mobile Number")
        mobile_no = input("Please enter your mobile number without any spaces or any characters: ")

    mpin = getpass("Please set a 6 digit mPIN for your account: ")
    while not check_mpin(mpin):
        print("Please enter a valid 6 digit numeric mPIN")
        mpin = getpass("Please set a 6 digit mPIN for your account: ")

    return {'name': name,
            'username': username,
            'address': address,
            'city': city,
            'state': state,
            'aadhaar': aadhaar,
            'mobile_no': mobile_no,
            'mpin': mpin}


def generating_account_number():
    """
    Generates 12 digit Account Number.
    """
    account_number = ""
    n = "1234567890"

    for i in range(12):
        account_number += n[randint(0, 9)]
    return account_number


def generating_cards():
    """
    Generated 3 digit cvv and 4 digit pin.
    :return: List containing cvv and pin.
    """
    n = "1234567890"
    card_cvv = ""
    card_pin = ""
    for i in range(3):
        card_cvv += n[randint(0, 9)]

    # credit or debit cards pin
    for i in range(4):
        card_pin += n[randint(0, 9)]

    return [card_cvv, card_pin]


def insert_user_info(name, username, address, city, state, aadhaar, mobile_no, account_number):
    """
    Insert the user information into users table in the database
    """
    insertion_query_users = f'''
        INSERT INTO users(name, username, address, city, state, aadhaar_number, mobile_no, account_number)
        VALUES('{name}', '{username}', '{address}', '{city}', '{state}', '{aadhaar}', '{mobile_no}', '{account_number}')
    '''
    mycursor.execute(insertion_query_users)
    mydb.commit()


def insert_debit_card_info(user_id, card_cvv, card_pin):
    """
    Insert the debit card information into cards table in the database
    """
    insertion_query_cards = f'''
        INSERT INTO cards(user_id, card_cvv, card_pin, card_type)
        VALUES( {user_id}, AES_ENCRYPT('{card_cvv}', 'pass'), AES_ENCRYPT('{card_pin}', 'pass'), 'debit')
    '''
    mycursor.execute(insertion_query_cards)
    mydb.commit()


def insert_credit_card_info(user_id, card_cvv, card_pin):
    """
    Insert the credit card information into cards table in the database
    """
    insertion_query_cards = f'''
        INSERT INTO cards(user_id, card_cvv, card_pin, card_type)
        VALUES( {user_id}, AES_ENCRYPT('{card_cvv}', 'pass'), AES_ENCRYPT('{card_pin}', 'pass'), 'credit')
    '''
    mycursor.execute(insertion_query_cards)
    mydb.commit()


def insert_balance_info(user_id, account_number, mpin):
    """
    Initialize the account with zero balance and updates the balance table
    """
    insertion_query_balance = f'''
        INSERT INTO balance(user_id, account_number, m_pin, balance)
        VALUES({user_id}, "{account_number}", AES_ENCRYPT('{mpin}', 'pass'), 0) 
    '''
    mycursor.execute(insertion_query_balance)
    mydb.commit()


def registering_user():
    """
    Takes all user information from registration_form() function.
    Insert the information into respective tables.
    Display user account information from bank_info database.
    """

    user_info = registration_form()

    name = user_info['name']
    username = user_info['username']
    address = user_info['address']
    city = user_info['city']
    state = user_info['state']
    aadhaar = user_info['aadhaar']
    mobile_no = user_info['mobile_no']
    mpin = user_info['mpin']

    account_number = generating_account_number()
    credit_card_info = generating_cards()
    credit_card_cvv = credit_card_info[0]
    credit_card_pin = credit_card_info[1]

    debit_card_info = generating_cards()
    debit_card_cvv = debit_card_info[0]
    debit_card_pin = debit_card_info[1]

    insert_user_info(name, username, address, city, state, aadhaar, mobile_no, account_number)

    getting_user_id = f'''
        SELECT id 
        FROM users
        WHERE account_number = {account_number}
    '''
    mycursor.execute(getting_user_id)
    user_id = mycursor.fetchone()[0]

    insert_debit_card_info(user_id, debit_card_cvv, debit_card_pin)
    insert_credit_card_info(user_id, credit_card_cvv, credit_card_pin)

    insert_balance_info(user_id, account_number, mpin)

    mycursor.execute(f"SELECT * FROM users WHERE account_number = {account_number}")
    result1 = mycursor.fetchone()
    print("Your account in XYZ Bank has been created.\nYour account information is mentioned below:")
    print(f"Name: {result1[1]}")
    print(f"username: {result1[2]}")
    print(f"Account Number: {result1[-1]}")

    mycursor.execute(f"SELECT * FROM balance WHERE user_id = {user_id} and account_number = {account_number}")
    result3 = mycursor.fetchall()

    for i in result3:
        print(f"Current Balance: {i[-1]}")

    login.login_menu()


def close_db():
    mycursor.close()
    mydb.close()
