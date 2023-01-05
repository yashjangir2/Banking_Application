# Banking Application
 

This is a Banking Application created using python and mySQL.

## prerequisites
1. python >= 3.8.2
2. mySQL >= 8.0.0

## install
```bash
pip3 install mysql-connector-python
```

## Usage
Run main.py file from the code base.

For adding some sample accounts into the database run random_test_accounts() function in creatingDB file after running main.py file once. 

## About Code

Contains 7 files in total

- #### main.py
    
  - **home_page()** :- Start of the application. User will be asked to login, register or exit.
                           Also closes all the mySQL servers once user exit the application.
  
- #### registration.py
     - **checking_name(name)** :- Takes name of the user as input and checks the validation of name. Name should contain only alphabets and length of name should be less than 100 characters.
     - **checking_only_username(username)** :- Checks the validation of the username provided by user i.e., checks that it contains only alphabets and "_" and length is less than 150 characters.
     - **checking_username(username)** :- Checks if the username given is already present in the table or not.
     - **checking_city(city)** :- Checks the validation of the city. City should contain only alphabets.
     - **checking_state(state)** :- Checks the validation of state. State should contain only alphabets.
     - **checking_aadhaar(aadhaar)** :- Checks aadhaar number should be 12 digit long and only contains numerics without any space or any characters. Input should be in string format.
     - **checking_mobile_no(mobile_no)** :- Checks that mobile number should be 10 digit long and contains only numerics. Also checks that mobile number format is valid in India. Input should be in string.
     - **checks_cvv(cvv)** :- Checks that CVV is 3 digit long and contains only numerics.
     - **checks_cvv_for_user(username, cvv)** :- Checks that CVV provided is owned by the user or not.
     - **checks_valid_pin(pin)** :- Checks that the pin is 4 digit long and contains only numerics.
     - **checks_pin(username, cvv, pin)** :-  Checks if user entered correct pin for the card of corresponding CVV.
     - **checks_account_number(account_number)** :- Checks that the account number is 12 digit long and only contains numerics.
     - **check_mpin(mpin)** :- Checks that mPIN contains only numerics and is 6 digit long.
     - **registration_form()** :- Takes user input for registration and checks their validation using above functions. Returns dictionary of user information if all the information are valid.
     - **generating_account_number()** :- Generates a 12 digit numeric account number. Returns account number in string format.
     - **generating_cards()** :- Generate a card's valid CVV and PIN. Returns a list containing CVV and pin.
     - **insert_user_info(name, username, address, city, state, aadhaar, mobile_no, account_number)** :- 
    
    