import mysql.connector
import creatingDB
import beneficiary
import registration
import updateDetails
from datetime import datetime
from getpass import getpass

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="1234",
    database="bank_info"
)
mycursor = mydb.cursor()


def get_user_id_from_acc_no(account_number):
    """
    Return user id of the account number
    """
    query = f'''
        SELECT id
        FROM users
        WHERE account_number = '{account_number}'
    '''
    mycursor.execute(query)
    result = mycursor.fetchone()
    mydb.commit()
    return result[0]


def get_acc_no_from_user_id(user_id):
    """
    Return account number of the user
    """
    query = f'''
        SELECT account_number
        FROM users
        WHERE id = {user_id}
    '''
    mycursor.execute(query)
    result = mycursor.fetchone()
    mydb.commit()
    return result[0]


def get_current_balance(user_id):
    """
    Returns current balance of user
    """
    query = f'''
        SELECT balance
        FROM balance
        WHERE user_id = {user_id}
    '''
    mycursor.execute(query)
    ans = mycursor.fetchone()
    mydb.commit()

    return ans[0]


def update_balance_for_user(user_id, amount):
    """
    Updates the current balance of user
    """
    try:
        query = f'''
            UPDATE balance
            SET balance = balance - {amount}
            WHERE user_id = {user_id}
        '''
        mycursor.execute(query)
        mydb.commit()

        return True
    except:
        return False


def update_balance_for_beneficiary(b_account_number, amount):
    """
    Update the balance for the beneficiary
    """
    try:
        query = f'''
            UPDATE balance
            SET balance = balance + {amount}
            WHERE account_number = '{b_account_number}'
        '''
        mycursor.execute(query)
        mydb.commit()

        return True
    except:
        return False


def transfer_money(username, account_number, b_name, b_account_number, amount):
    """
    Transfers money to the account number provided
    """
    user_id = updateDetails.get_user_id(username)

    if int(amount) > get_current_balance(user_id):
        print("Insufficient Funds!!!")
    else:
        current_balance = get_current_balance(user_id)
        t1 = update_balance_for_user(user_id, amount)

        if t1:
            c_b_balance = get_current_balance(get_user_id_from_acc_no(b_account_number))
            t2 = update_balance_for_beneficiary(b_account_number, amount)
            if t2:
                print("Transaction Successful")
                print(f"{amount} has been debited from your account")
                entry_in_transactions_table(user_id, account_number, b_name, b_account_number, amount)
            else:
                p_balance = get_current_balance(get_user_id_from_acc_no(b_account_number))
                if c_b_balance == p_balance:
                    query = f'''
                        UPDATE balance
                        SET balance = balance + {amount}
                        WHERE user_id = {user_id}
                    '''
                    mycursor.execute(query)
                    mydb.commit()
                else:
                    print("Transaction Successful")
                    print(f"{amount} has been debited from your account")
                    entry_in_transactions_table(user_id, account_number, b_name, b_account_number, amount)

        else:
            p_balance = get_current_balance(user_id)
            if p_balance != current_balance:
                query = f'''
                            UPDATE balance
                            SET balance = balance + {amount}
                            WHERE user_id = {user_id}
                        '''
                mycursor.execute(query)
                mydb.commit()


def authenticate_user(user_id, pin):
    """
    Verify the mPIN of the user
    """
    query = f'''
        SELECT balance, account_number
        FROM balance
        WHERE user_id = {user_id} and CAST(AES_DECRYPT(m_pin, '{creatingDB.encryption_pass()}') AS CHAR) = '{pin}'
    '''
    mycursor.execute(query)
    result = mycursor.fetchall()

    if len(result) == 0:
        return False
    return True


def entry_in_transactions_table(user_id, account_number,  b_name, b_account_number, amount):
    """
    Updates the transactions table
    """
    now = datetime.now()
    dt_string = now.strftime("%Y-%m/%d %H:%M:%S")

    query = f'''
        INSERT INTO transactions(user_id, account_number, beneficiary_name, 
                beneficiary_account_number, amount, timestamp)
        VALUES({user_id}, '{account_number}', '{b_name}', '{b_account_number}', {amount}, '{dt_string}')
    '''
    mycursor.execute(query)
    mydb.commit()


def take_user_information(username):
    """
    Takes user input and checks its validation
    User have to select between 1 and 2. if user selects one we don't ask for account number and
    if user press 2 we will ask user account number and name whom the funds is to be transferred.
    """
    user_id = updateDetails.get_user_id(username)
    account_number = get_acc_no_from_user_id(user_id)

    beneficiaries = beneficiary.list_beneficiaries(username)
    if len(beneficiaries) != 0:
        print("Press 1 if you want to transfer money to one of the beneficiary.")
        print("Press 2 to transfer money to another account: ")

        t = input("Key: ")
        while not t.isnumeric() or len(t) != 1 or int(t) < 0 or int(t) > 2:
            print("Please enter a valid key.")
            t = input("Key: ")

        if int(t) == 2:
            b_name = input("Please enter Name: ")
            while not registration.checking_name(b_name):
                print("Please enter a valid name")
                b_name = input("Please enter Name: ")

            b_account_number = input("Please enter account number: ")
            while not registration.checks_account_number(b_account_number):
                print("Please enter a valid account number")
                b_account_number = input("Please enter account number: ")

            if not beneficiary.checks_beneficiary_and_account_no(b_name, b_account_number):
                print("Invalid name and account number")

            elif get_user_id_from_acc_no(b_account_number) == updateDetails.get_user_id(username):
                print("Cannot transfer funds to yourself!!!")
            else:
                print("Press 1 to add this account as beneficiary else press 0")
                t = input("Key: ")
                while not t.isnumeric() or int(t) > 1 or int(t) < 0:
                    print("Invalid Key!!!")
                    t = input("Key: ")

                if int(t) == 1:
                    beneficiary.add_beneficiary(username, b_name, b_account_number)
                    print("Beneficiary Added")

                amount = input("Please enter the amount: ")
                while not amount.isnumeric():
                    print("Please enter a valid amount")
                    amount = input("Please enter the amount: ")

                m_pin = getpass("Please enter you mPIN: ")
                while not registration.check_mpin(m_pin):
                    print("Please enter a valid mPIN")
                    m_pin = getpass("Please enter you mPIN: ")

                if authenticate_user(user_id, m_pin):
                    transfer_money(username, account_number, b_name, b_account_number, amount)
        elif int(t) == 1:
            for i in range(0, len(beneficiaries)):
                print(f"Press {i + 1} to transfer money to {beneficiaries[i][0]}")

            t = input("Key: ")
            while not t.isnumeric() or int(t) < 0 or int(t) > len(beneficiaries):
                print("Please enter a valid key")
                t = input("Key: ")

            for i in range(len(beneficiaries)):
                if int(t) == i + 1:
                    b_name = beneficiaries[i][0]
                    b_account_number = beneficiaries[i][1]

                    amount = input("Please enter the amount: ")
                    while not amount.isnumeric():
                        print("Please enter a valid amount")
                        amount = input("Please enter the amount: ")

                    m_pin = getpass("Please enter you mPIN: ")
                    while not registration.check_mpin(m_pin):
                        print("Please enter a valid mPIN")
                        m_pin = getpass("Please enter you mPIN: ")

                    if authenticate_user(user_id, m_pin):
                        transfer_money(username, account_number, b_name, b_account_number, amount)

    else:
        b_name = input("Please enter the name of beneficiary: ")
        while not registration.checking_name(b_name):
            print("Please enter a valid name")
            b_name = input("Please enter the name of beneficiary: ")

        b_account_number = input("Please enter beneficiary account number: ")
        while not registration.checks_account_number(b_account_number):
            print("Please enter a valid account number")
            b_account_number = input("Please enter beneficiary account number: ")

        if not beneficiary.checks_beneficiary_and_account_no(b_name, b_account_number):
            print("Invalid name and account number")

        elif get_user_id_from_acc_no(b_account_number) == updateDetails.get_user_id(username):
            print("Cannot transfer funds to yourself!!!")
        else:
            print("Press 1 to add this account as beneficiary else press 0")
            t = input("Key: ")
            while not t.isnumeric() or int(t) > 1 or int(t) < 0:
                print("Invalid Key!!!")
                t = input("Key: ")

            if int(t) == 1:
                beneficiary.add_beneficiary(username, b_name, b_account_number)
                print("Beneficiary Added")

            amount = input("Please enter the amount: ")
            while not amount.isnumeric():
                print("Please enter a valid amount")
                amount = input("Please enter the amount: ")

            m_pin = getpass("Please enter you mPIN: ")
            while not registration.check_mpin(m_pin):
                print("Please enter a valid mPIN")
                m_pin = getpass("Please enter you mPIN: ")

            if authenticate_user(user_id, m_pin):
                transfer_money(username, account_number, b_name, b_account_number, amount)


def close_db():
    mycursor.close()
    mydb.close()