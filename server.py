#this code is under development

import pymysql
import sys
import flask
import json

app=flask.Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def login():
    msg_received = flask.request.get_json()
    msg_subject = msg_received["subject"]

    if msg_subject == "register":
        return register(msg_received)
    elif msg_subject == "login":
        return login(msg_received)
    else:
        return "Invalid request."

def register(msg_received):
    firstname = msg_received["firstname"]
    lastname = msg_received["lastname"]
    mobileno = msg_received["mobileno"]
    password = msg_received["password"]

    select_query = "SELECT * FROM logins where phone_no = " + "'" + mobileno + "'"
    db_cursor.execute(select_query)
    records = db_cursor.fetchall()
    if len(records) != 0:
        return "User already exists"
    insert_query = "INSERT INTO logins (first_name, last_name, phone_no, password) VALUES (%s, %s, %s, MD5(%s))"
    insert_values = (firstname, lastname, mobileno, password)

    try:
        db_cursor.execute(insert_query, insert_values)
        login_db.commit()
        return "success"
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"

def login(msg_received):
    mobileno = msg_received["mobileno"]
    password = msg_received["password"]

    select_query = "SELECT first_name, last_name FROM logins where phone_no = " + "'" + mobileno + "' and password = " + "MD5('" + password + "')"
    db_cursor.execute(select_query)
    records = db_cursor.fetchall()

    if len(records) == 0:
        return "failure"
    else:
        return "success"


login_db = pymysql.connect(host="localhost", port=3306, user="root", password="root",db="login") 

db_cursor=login_db.cursor()

app.run(host="0.0.0.0", port=6000, threaded=True)