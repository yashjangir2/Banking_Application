import mysql.connector
import main

try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="1234"
    )
    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS bank_info")
except:
    print("Something went wrong!!")


def creating_all_tables():
    """
    Creates the MySQL database and the necessary tables required
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="bank_info"
    )
    mycursor = mydb.cursor()

    # USERS TABLE
    create_users_table = '''
        CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            username VARCHAR(150),
            address TEXT,
            city VARCHAR(50),
            state VARCHAR(50),
            aadhaar_number VARCHAR(15),
            mobile_no VARCHAR(12),
            account_number VARCHAR(15)
        )
    '''
    mycursor.execute(create_users_table)

    # CARDS TABLE
    create_cards_table = '''
        CREATE TABLE IF NOT EXISTS cards(id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            card_cvv blob,
            card_pin blob,
            card_type ENUM("credit", "debit"),
            FOREIGN KEY(user_id) REFERENCES users(id)
            ON DELETE CASCADE
        )
    '''
    mycursor.execute(create_cards_table)

    # BALANCE TABLE
    create_balance_table = '''
        CREATE TABLE IF NOT EXISTS balance(id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            account_number VARCHAR(15),
            m_pin blob,
            balance INT,
            FOREIGN KEY(user_id) REFERENCES users(id)
            ON DELETE CASCADE
        )
    '''
    mycursor.execute(create_balance_table)

    # BENEFICIARY TABLE
    create_beneficiary_table = '''
        CREATE TABLE IF NOT EXISTS beneficiary(id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            username VARCHAR(150),
            beneficiary_name VARCHAR(100),
            beneficiary_account_number VARCHAR(15),
            FOREIGN KEY(user_id) REFERENCES users(id)
            ON DELETE CASCADE
        )
    '''
    mycursor.execute(create_beneficiary_table)

    # TRANSACTIONS TABLE
    create_transactions_table = '''
        CREATE TABLE IF NOT EXISTS transactions(id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            account_number VARCHAR(15),
            beneficiary_name VARCHAR(100),
            beneficiary_account_number VARCHAR(15),
            amount INT,
            timestamp DATETIME,
            FOREIGN KEY(user_id) REFERENCES users(id)
            ON DELETE CASCADE
        )
    '''
    mycursor.execute(create_transactions_table)

    mycursor.close()
    mydb.close()


def random_test_accounts():
    """
    Inserts some random test accounts into the database for testing
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="bank_info"
    )
    mycursor = mydb.cursor()

    insert_users = '''
        INSERT INTO users(name, username, address, city, state, aadhaar_number, mobile_no, account_number)
        VALUES ("X Yz", "a_b_c", "qwerty", "delhi", "delhi", "111221111111", "8778723131", "123456789012"),
        ("Peter", "abc_abc", "There", "That", "This", "111222231111", "8123312313", "000000000000"),
        ("Abc Xyz", "hello", "that street", "mumbai", "maharashtra", "432234231342", "7123657423", "111111111111"),
        ("Tiger", "tiger_h", "this street", "lucknow", "uttar pradesh", "444321331111", "9234412999", "222222222222"),
        ("Poacher", "hello_world", "Tiger street", "That", "This", "999772231234", "9993123000", "333333333333")
    '''
    mycursor.execute(insert_users)
    mydb.commit()

    insert_cards = f'''
        INSERT INTO cards(user_id, card_cvv, card_pin, card_type)
        VALUES ((SELECT id from users where account_number = '123456789012'),
                AES_ENCRYPT('123', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'debit'),
        ((SELECT id from users where account_number = '123456789012'), 
                AES_ENCRYPT('999', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'credit'),
        ((SELECT id from users where account_number = '000000000000'), 
                AES_ENCRYPT('000', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'debit'),
        ((SELECT id from users where account_number = '000000000000'), 
                AES_ENCRYPT('111', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'credit'),
        ((SELECT id from users where account_number = '111111111111'), 
                AES_ENCRYPT('222', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'debit'),
        ((SELECT id from users where account_number = '111111111111'), 
                AES_ENCRYPT('333', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'credit'),
        ((SELECT id from users where account_number = '222222222222'), 
                AES_ENCRYPT('444', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'debit'),
        ((SELECT id from users where account_number = '222222222222'), 
                AES_ENCRYPT('555', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'credit'),
        ((SELECT id from users where account_number = '333333333333'), 
                AES_ENCRYPT('666', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'debit'),
        ((SELECT id from users where account_number = '333333333333'), 
                AES_ENCRYPT('777', '{main.encryption_pass()}'), AES_ENCRYPT('1234', '{main.encryption_pass()}'), 'credit')
    '''
    mycursor.execute(insert_cards)
    mydb.commit()

    insert_balance = f'''
            INSERT INTO balance(user_id, account_number, m_pin, balance)
            VALUES ((SELECT id from users where account_number = '123456789012'), 
                    "123456789012", AES_ENCRYPT('123456', '{main.encryption_pass()}'), 100002),
            ((SELECT id from users where account_number = '000000000000'), 
                    "000000000000", AES_ENCRYPT('000000', '{main.encryption_pass()}'), 500002),
            ((SELECT id from users where account_number = '111111111111'), 
                    "111111111111", AES_ENCRYPT('111111', '{main.encryption_pass()}'), 10000),
            ((SELECT id from users where account_number = '222222222222'), 
                    "222222222222", AES_ENCRYPT('222222', '{main.encryption_pass()}'), 99999),
            ((SELECT id from users where account_number = '333333333333'), 
                    "333333333333", AES_ENCRYPT('333333', '{main.encryption_pass()}'), 1000000)
        '''
    mycursor.execute(insert_balance)
    mydb.commit()

    mycursor.close()
    mydb.close()


# random_test_accounts()


def close_db():
    mycursor.close()
    mydb.close()
