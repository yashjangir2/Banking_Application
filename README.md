# Banking Application
 

This is a Banking Application created using python and mySQL.

## Table of contents
- [Prerequesites](#prerequisites)
- [Installations](#installations)
- [Usage](#usage)
- [About Code](#about-code)

   - [creatingDB.py](#creatingDBpy)
   - [main.py](#mainpy)
   - [registration.py](#registrationpy)
   - [login.py](#loginpy)
   - [updateDetails.py](#updateDetailspy)
   - [beneficiary.py](#beneficiarypy)
   - [transferFunds.py](#transferFundspy)

## prerequisites
1. python >= 3.8.2
2. mySQL >= 8.0.0

## installations
```bash
pip3 install mysql-connector-python
```

## Usage
Before starting the application connect to your mySQL server in every file.
In creatingDB.py file please connect to server in creating_all_tables() and random_test_accounts() functions to connect to the database once it is created.

Run main.py file from the code base to start the application.

For adding some sample accounts into the database run random_test_accounts() function in creatingDB file after running main.py file once. 

## About Code

Contains 7 main files in total.

Description of functions and files are given below: 

- #### creatingDB.py
    This file creates the database once we run the application.
  - ***creating_all_tables()*** :- Creates all the tables required in the database.
  - ***random_test_accounts()*** :- Adds some test entries in the database.
- #### main.py
    
  - ***home_page()*** :- Start of the application. User will be asked to login, register or exit.
                           Also closes all the mySQL servers once user exit the application.
  
- #### registration.py
     - ***checking_name(name)*** :- Takes name of the user as input and checks the validation of name. Name should contain only alphabets and length of name should be less than 100 characters.
     - ***checking_only_username(username)*** :- Checks the validation of the username provided by user i.e., checks that it contains only alphabets and "_" and length is less than 150 characters.
     - ***checking_username(username)*** :- Checks if the username given is already present in the table or not.
     - ***checking_city(city)*** :- Checks the validation of the city. City should contain only alphabets.
     - ***checking_state(state)*** :- Checks the validation of state. State should contain only alphabets.
     - ***checking_aadhaar(aadhaar)*** :- Checks aadhaar number should be 12 digit long and only contains numerics without any space or any characters. Input should be in string format.
     - ***checking_mobile_no(mobile_no)*** :- Checks that mobile number should be 10 digit long and contains only numerics. Also checks that mobile number format is valid in India. Input should be in string.
     - ***checks_cvv(cvv)*** :- Checks that CVV is 3 digit long and contains only numerics.
     - ***checks_cvv_for_user(username, cvv)*** :- Checks that CVV provided is owned by the user or not.
     - ***checks_valid_pin(pin)*** :- Checks that the pin is 4 digit long and contains only numerics.
     - ***checks_pin(username, cvv, pin)*** :-  Checks if user entered correct pin for the card of corresponding CVV.
     - ***checks_account_number(account_number)*** :- Checks that the account number is 12 digit long and only contains numerics.
     - ***check_mpin(mpin)*** :- Checks that mPIN contains only numerics and is 6 digit long.
     - ***registration_form()*** :- Takes user input for registration and checks their validation using above functions. Returns dictionary of user information if all the information are valid.
     - ***generating_account_number()*** :- Generates a 12 digit numeric account number. Returns account number in string format.
     - ***generating_cards()*** :- Generate a card's valid CVV and PIN. Returns a list containing CVV and pin.
     - ***insert_user_info(name, username, address, city, state, aadhaar, mobile_no, account_number)*** :- Insert the user information into users table in the database.
     - ***insert_debit_card_info(user_id, card_cvv, card_pin)*** :- Insert the debit card information into cards table in the database.
     - ***insert_credit_card_info(user_id, card_cvv, card_pin)*** :- Insert the credit card information into cards table in the database.
     - ***insert_balance_info(user_id, account_number, mpin)*** :- Initialize the account with zero balance and inserts the information in balance table.
     - ***registering_user()*** :- Takes all user information from registration_form() function. Insert the information into respective tables using the insert functions mentioned above. Also display user account information from bank_info database once the data is successfully uploaded in the database.
- #### login.py
     - ***checking_login_details(username, pin)*** :- Checks the login credentials entered are correct or not.
     - ***list_bank_details(username)*** :- Returns the list of tuples containing information like username, account_number, mobile number, CVV and card type.
     - ***list_card_cvvs(username)*** :- Returns the list of all card CVVs owned by user.
     - ***display_details(username)*** :-  Prints the user information corresponding to the username provided. Prints list of cards, list of beneficiaries, current balance, and username.
     - ***update_details(username)*** :- Update user's address, city, state and mobile number. Also checks validation of new entries provided by user.
     - ***change_pin(username)*** :- changes pin of the card. Also checks validation of the new pin entered by user.
     - ***add_credit_card(username)*** :- Takes input for the pin of new card generated and checks its validation. Adds a new credit in the database for the user using *add_new_credit_card(username, pin)* function from *updateDetails.py*.
     - ***add_beneficiary_2(username)*** :-  Checks validation of name and account number of the beneficiary. Also checks if the beneficiary is present in the database or not. After all validations insert the beneficiary into beneficiary table using add_beneficiary()
    function in beneficiary file.
     - ***transfer_money(username)*** :- Transfer money to another account using take_user_information(username) function from transferFunds.py.
     - ***change_mpin(username)*** :- Takes current mPIN and new mPIN from user and checks their validation and changes the mPIN and updates in the database using change_mpin(username, new_mpin) function in updateDetails.py.
     - ***transaction_details(username)*** :- Displays transaction details of the user.
     - ***login_functions(username)*** :- Asks user to which action to perform by taking input after he/she logs in.
     - ***login_menu()*** :- Takes username and mPIN from users to log in into the account if all information provided are correct. Also checks the validation of information entered.
- #### updateDetails.py
     - ***get_user_id(username)***:- Returns user id of the user with the given username.
     - ***update_address(username, new_address)***:- Updates the address of the username provided.
     - ***update_city(username, new_city)*** :-  Updates the city of the username provided
     - ***update_state(username, new_state)*** :- Updates the state of the username provided
     - ***update_mobile_no(username, new_mobile_no)*** :-  Updates the mobile number of the username provided
     - ***change_pin(username, cvv, pin, new_pin)*** :-  Changes the pin of the card user provided. Also checks validation of new_pin.
     - ***add_new_credit_card(username, pin)*** :- Adds new credit card for the user in the database.
     - ***change_mpin(username, new_mpin)*** :- changes mPIN and updates in the database.
- #### beneficiary.py
     - ***checks_beneficiary_and_account_no(b_name, b_account_number)*** :- Checks beneficiary name and account number if they are present in the database i.e., in users table or not.
     - ***check_beneficiary_for_user(username, b_name, b_account_number)*** :- Checks if beneficiary is already added by the user or not.
     - ***add_beneficiary(username, name, b_account_number)*** :- Adds beneficiary to the beneficiary table if it is not added by the user and is present in users table.
     - ***list_beneficiaries(username)*** :- Returns the list of beneficiaries containing beneficiary name and account number.
     - ***print_beneficiaries(username)*** :- Prints the details of all beneficiaries.
- #### transferFunds.py
 
     - ***get_user_id_from_acc_no(account_number)***:-  Return user id of the account number given.
     - ***get_acc_no_from_user_id(user_id)*** :- Return account number using user id.
     - ***get_current_balance(user_id)*** :- Returns current balance of user.
     - ***update_balance_for_user(user_id, amount)*** :- Updates the current balance of user once transaction is made.
     - ***update_balance_for_beneficiary(b_account_number, amount)*** :- Updates the balance of beneficiary.
     - ***transfer_money(username, account_number, b_name, b_account_number, amount)*** :- Checks the transactions i.e., if any transactions fails make sure that the current balance of users is not affected.
     - ***authenticate_user(user_id, pin)*** :- checks the mPIN of user.
     - ***entry_in_transactions_table(user_id, account_number,  b_name, b_account_number, amount)*** :- Inserts information in transaction table.
     - ***take_user_information(username)*** :- Takes information from user to transfer money and checks the validation of information provided.
