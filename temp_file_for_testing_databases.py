import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="bank_info"
)

mycursor = mydb.cursor()

# Creating users table in sql database.
# query = '''
#    CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY AUTO_INCREMENT,
#         name VARCHAR(100),
#         address TEXT,
#         aadhaar_number VARCHAR(15),
#         mobile_no VARCHAR(12),
#         account_number VARCHAR(15)
#     )
# '''

# mycursor.execute('SELECT * FROM users')
mycursor.execute('SELECT CAST(AES_DECRYPT(card_pin, "pass") AS CHAR) FROM cards')
result = mycursor.fetchall()
for i in result:
  print(i)
