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


def is_logged_in():
    if session.get('email') is None:
        print('logged out')
        return False
    else:
        print('logged in')
        return True


@app.route('/')
def home():
    return render_template('home.html', categories=get_categories(), logged_in=is_logged_in())


def get_categories():
    con = create_connection(DATABASE)
    query = "SELECT id, name FROM categories"
    cur = con.cursor()
    cur.execute(query)
    categories = cur.fetchall()
    con.close()
    return categories


@app.route('/category/<catID>')
def render_home1(catID):
    con = create_connection(DATABASE)
    query = "SELECT id, maori, english, image FROM words WHERE category_id=? ORDER BY maori ASC"
    cur = con.cursor()
    cur.execute(query, (catID, ))
    word_list = cur.fetchall()
    con.close
    return render_template("category.html", logged_in=is_logged_in(), categories=get_categories(), words=word_list)


@app.route('/word/<wordID>')
def render_home2(wordID):
    con = create_connection(DATABASE)
    query = "SELECT id, maori, english, image, definition, level, category_id FROM words WHERE id=? ORDER BY maori ASC"
    cur = con.cursor()
    cur.execute(query, (wordID, ))
    word_list = cur.fetchall()
    con.close
    return render_template("words.html", logged_in=is_logged_in(), categories=get_categories(), words=word_list)


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


@app.route('/logout')
def logout():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect('/')


def get_categories():
    con = create_connection(DATABASE)
    print(con)
    query = "SELECT id, category FROM categories ORDER BY category ASC"
    cur = con.cursor()
    cur.execute(query)
    category_list = cur.fetchall()
    con.close()
    return category_list


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        print(request.form)
        first_name = request.form.get('first_name').title().strip()
        surname = request.form.get('surname').title().strip()
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('confirm_password')
        teacher = request.form.get('teacher')

        if password != password2:
            return redirect("/signup?error=Please+make+password+match")

        if len(password) < 8:
            return redirect("/signup?error=Please+make+password+at+least+8+characters")

        if teacher == 'teacher':
            teacher = 1
        else:
            teacher = 0

        con = create_connection(DATABASE)

        query = "INSERT INTO users (first_name, last_name, email, password, teacher) VALUES (?, ?, ?, ?, ?)"
        cur = con.cursor()
        cur.execute(query, (first_name, surname, email, password, teacher))
        con.commit()
        con.close()
        return redirect("/")

    error = request.args.get('error')
    if error == None:
        error = ""

    return render_template("signup.html", error=error)


if __name__ == '__main__':
    app.run()



