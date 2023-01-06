import mysql.connector

import transferFunds
import updateDetails

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="1234",
    database="bank_info"
)
mycursor = mydb.cursor()


def checks_beneficiary_and_account_no(b_name, b_account_number):
    """
    Checks beneficiary name and account number if they are present in the database or not
    :return: True if present else False
    """
    query = f'''
        SELECT *
        FROM users
        WHERE name = '{b_name}' AND account_number = '{b_account_number}'
    '''
    mycursor.execute(query)
    result = mycursor.fetchall()
    if len(result) == 0:
        return False
    return True


def check_beneficiary_for_user(username, b_name, b_account_number):
    """
    Checks if beneficiary is already added by the user or not.
    Return True if beneficiary present else False.
    """
    if (b_name, b_account_number) in list_beneficiaries(username):
        return True
    return False


def add_beneficiary(username, name, b_account_number):
    """
    Adds beneficiary to the beneficiary table
    """
    user_id = updateDetails.get_user_id(username)

    if not check_beneficiary_for_user(username, name, b_account_number) \
            and b_account_number != transferFunds.get_acc_no_from_user_id(user_id):
        query = f'''
            INSERT INTO beneficiary(user_id, username, beneficiary_name, beneficiary_account_number)
            VALUES ({user_id}, '{username}', '{name}', '{b_account_number}')
        '''
        mycursor.execute(query)
        mydb.commit()
    elif b_account_number == transferFunds.get_acc_no_from_user_id(user_id):
        print("Cannot add yourself as beneficiary")
    else:
        print("Beneficiary already present")


def list_beneficiaries(username):
    """
    Returns the list of all beneficiaries
    """
    user_id = updateDetails.get_user_id(username)
    query = f'''
            SELECT beneficiary_name, beneficiary_account_number
            FROM beneficiary
            WHERE user_id = {user_id}
        '''
    mycursor.execute(query)
    result = mycursor.fetchall()

    return result


def print_beneficiaries(username):
    """
    Prints the list of all beneficiaries of the user
    """
    user_id = updateDetails.get_user_id(username)
    query = f'''
        SELECT *
        FROM beneficiary
        WHERE user_id = {user_id}
    '''
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.commit()

    count = 1
    print("List of beneficiaries")
    for i in result:
        print(f"{count}. {i[-2]}: {i[-1]}")
        count += 1


def close_db():
    mycursor.close()
    mydb.close()