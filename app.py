from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from datetime import datetime


app = Flask(__name__)
DATABASE = "C:/Users/18077/OneDrive - Wellington College/13DTS/Maori-dictionary/dicitionary.db"
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


@app.route('/login', methods=['POST', 'GET'])
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


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        print(request.form)
        first_name = request.form.get('first_name').title().strip()
        surname = request.form.get('surname').title().strip()
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('confirm_password')

        if password != password2:
            return redirect("/signup?error=Please+make+password+match")

        if len(password) < 8:
            return redirect("/signup?error=Please+make+password+at+least+8+characters")

        con = create_connection(DATABASE)

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)"
        cur = con.cursor()
        cur.execute(query, (first_name, surname, email, password))
        con.commit()
        con.close()
        return redirect("/")

    error = request.args.get('error')
    if error == None:
        error = ""

    return render_template("signup.html", error=error)


if __name__ == '__main__':
    app.run()



