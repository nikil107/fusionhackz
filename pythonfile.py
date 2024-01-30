from flask import Flask, request
import sqlite3
import random

app = Flask(__name__)

conn = sqlite3.connect('members.db')
cursor = conn.cursor()
@app.route("/")

def data_input():
    name = input("Enter the name     : ")
    u_name = input("Enter the username : ")
    password = input("Enter the password : ")
    email = input("Enter the e-mail   : ")
    phone = input("Enter the Phone no : ")
    token_bal = input("token balance  : ")
    inputs = (name, u_name, password, email, phone, token_bal)
    cursor.execute("INSERT INTO d_base (name, u_name, password, email, phone, token_bal) VALUES (?, ?, ?, ?, ?, ?)", inputs)

def clear_all():
    cursor.execute("DELETE FROM d_base")

def check_bal(u_name):
    cursor.execute("SELECT * FROM d_base WHERE u_name = ?", (u_name,))
    record = cursor.fetchone()
    print(f"{record[0]} : {record[5]} tokens")

def delete_record(user_name):
    cursor.execute("DELETE FROM d_base WHERE u_name = ?", (user_name,))

def update(user_name, token_bal):
    cursor.execute("UPDATE d_base SET token_bal = ? WHERE u_name = ?", (token_bal, user_name,))

def transaction(u_name_send, u_name_receive, transfer_amt):
    transfer_id = random.randrange(10 ** 9, 10 ** 10)
    cursor.execute("INSERT INTO transactions (sender, receiver, transfer, transfer_id) VALUES (?, ?, ?, ?)",
                   (u_name_send, u_name_receive, transfer_amt, transfer_id))
    cursor.execute("SELECT * FROM d_base WHERE u_name = ?",(u_name_send,))
    record = cursor.fetchone()
    cursor.execute("UPDATE d_base SET token_bal = ? WHERE u_name = ?", (str(int(record[5])-int(transfer_amt)), u_name_send,))
    cursor.execute("SELECT * FROM d_base WHERE u_name = ?", (u_name_receive,))
    record = cursor.fetchone()
    cursor.execute("UPDATE d_base SET token_bal = ? WHERE u_name = ?",
                   (str(int(record[5]) + int(transfer_amt)), u_name_receive,))

def generate_token(u_name, amt):
    cursor.execute("SELECT * FROM d_base WHERE u_name = ?", (u_name,))
    record = cursor.fetchone()
    cursor.execute("UPDATE d_base SET token_bal = ? WHERE u_name = ?",
                   (str(int(record[5]) + int(amt)), u_name,))

def admin_bal_set(u_name, amt):
    cursor.execute("SELECT * FROM d_base WHERE u_name = ?", (u_name,))
    record = cursor.fetchone()
    cursor.execute("UPDATE d_base SET token_bal = ? WHERE u_name = ?",
                   (str(amt), u_name,))

cursor.execute("CREATE TABLE IF NOT EXISTS d_base (name TEXT, u_name TEXT,password TEXT,email TEXT,phone TEXT,token_bal TEXT);")
cursor.execute("CREATE TABLE IF NOT EXISTS transactions (sender TEXT, receiver TEXT,transfer TEXT,transfer_id TEXT);")

#///////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////

conn.commit()
cursor.execute("SELECT * FROM d_base")
data = cursor.fetchall()
for i in data:
    print(i)

conn.close()

if __name__ == "__main__":
    app.run(debug=True)
