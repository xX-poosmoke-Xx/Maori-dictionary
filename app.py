from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from datetime import datetime


app = Flask(__name__)
DATABASE = "smile.db"
app.secret_key = "jittrippin"


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')

        con = create_connection(DATABASE)
        query = 'SELECT id, first_name FROM users WHERE email=? AND password=?'
        cur = con.cursor()
        cur.execute(query, (email, password))
        user_data = cur.fetchall()
        con.close()

        if user_data:
            user_id = user_data[0][0]
            first_name = user_data[0][1]
            print(user_id, first_name)

            session['email'] = email
            session['userid'] = user_id
            session['first_name'] = first_name

            return redirect("/")

        else:
            return redirect("/login?error=Incorrect+username+or+password")

    return render_template("login.html")


if __name__ == '__main__':
    app.run()



