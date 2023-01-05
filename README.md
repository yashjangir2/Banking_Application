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

## About code

Contains 7 files in total

- main.py
    
  - *home_page()* :- Start of the application. User will be asked to login, register or exit.
                           Also closes all the mySQL servers once user exit the application.
  
- registration.py
     - *checking_name(name)* :- Takes name of the user as input and checks the validation of name. Name should contain only alphabets and length of name should be less than 100 characters.
     - *checking_only_username(username)* :- Checks the validation of the username provided by user i.e., checks that it contains only alphabets and "_" and length is less than 150 characters.
     - *checking_username(username)* :- Checks if the username given is already present in the table or not.
     - *checking_city(city)* :- Checks the validation of the city. City should contain only alphabets.
     - **
    
    