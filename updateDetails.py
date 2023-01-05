import mysql.connector
import registration


mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="1234",
    database="bank_info"
)
mycursor = mydb.cursor()


def checks_username(username):
    """
    Checks if the user with the username exists or not
    :return: True if exists else False
    """
    user_id_q = f'''
        SELECT id
        FROM users
        WHERE username = "{username}"
    '''
    mycursor.execute(user_id_q)
    user_id = mycursor.fetchone()
    if len(user_id) == 0:
        return False
    return True


def get_user_id(username):
    """
    Returns user id of the user with the given username
    """
    user_id_q = f'''
        SELECT id
        FROM users
        WHERE username = "{username}"
    '''
    mycursor.execute(user_id_q)
    user_id = mycursor.fetchone()[0]
    return user_id


def update_address(username, new_address):
    """
    Updates the address of the username provided
    """
    query = f'''
        UPDATE users
        SET address = '{new_address}'
        WHERE username = '{username}'
    '''
    mycursor.execute(query)
    mydb.commit()


def update_city(username, new_city):
    """
    Updates the city of the username provided
    """
    query = f'''
        UPDATE users
        SET city = '{new_city}'
        WHERE username = '{username}'
    '''
    mycursor.execute(query)
    mydb.commit()


def update_state(username, new_state):
    """
    Updates the state of the username provided
    """
    query = f'''
        UPDATE users
        SET state = '{new_state}'
        WHERE username = '{username}'
    '''
    mycursor.execute(query)
    mydb.commit()


def update_mobile_no(username, new_mobile_no):
    """
    Updates the mobile number of the username provided
    """
    query = f'''
        UPDATE users
        SET mobile_no = '{new_mobile_no}'
        WHERE username = '{username}'
    '''
    mycursor.execute(query)
    mydb.commit()


def change_pin(username, cvv, pin, new_pin):
    """
    Changes the pin of the card user provided. Also checks validation of new_pin
    """
    user_id = get_user_id(username)

    query = f'''
        UPDATE cards
        SET card_pin = '{new_pin}'
        WHERE user_id = {user_id} AND card_cvv = {cvv} AND card_pin = '{pin}'
    '''
    mycursor.execute(query)
    mydb.commit()


def add_new_credit_card(username, pin):
    """
    Adds new credit card for the user in the database
    """
    if checks_username(username):
        user_id = get_user_id(username)
        new_card_details = registration.generating_cards()

        query = f'''
            INSERT INTO cards(user_id, card_cvv, card_pin, card_type)
            VALUES ({user_id}, {new_card_details[0]}, '{pin}', 'credit')
        '''
        mycursor.execute(query)
        mydb.commit()

        return new_card_details[0]
    else:
        print("User doesn't exist!!")
        return 0


def change_mpin(username, new_mpin):
    """
    changes mPIN and updates in the database
    """
    user_id = get_user_id(username)
    query = f'''
        UPDATE balance
        SET m_pin = '{new_mpin}'
        WHERE user_id = {user_id}
    '''
    mycursor.execute(query)
    mydb.commit()


def close_db():
    mycursor.close()
    mydb.close()