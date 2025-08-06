from flask import Flask, render_template, redirect, request, url_for, session, g, jsonify
import sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'secret'
bcrypt = Bcrypt(app)

def connect_db():
    sql = sqlite3.connect('./database.db')
    sql.row_factory = sqlite3.Row #changes from dict to tuple... makes easier to read
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
        return g.sqlite3_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite3'):
        g.sqlite3_db.close()




@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/login",methods=["GET", "POST"])
def login():
    return render_template("login.html")
        

@app.route("/store")
def store():
    if not session.pop('from-login', False):
        return redirect(url_for('login'))
    return render_template("store.html")



@app.route("/create-account")
def create_account():
    return render_template('create-account.html')


@app.route("/submit-form", methods=["GET"])
def authenticate():
    Username = request.form["Username"]
    Password = request.form["Password"]

    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE email = ?', (Username,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user['password'], Password):
        session['from-login'] = True
        return redirect(url_for('store'))
    else:
        return redirect(url_for('login'))

    

@app.route("/submit-account", methods=["GET","POST"])
def check_account():

    data = request.get_json()

    email = data.get("New_Email")
    password = data.get("New_Password")


    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE email = ?', (email,))
    rows = cursor.fetchall()

    #THE CODE BELOW IS FOR TESTING PURPOUSES. WILL GET SENT A EMAIL IN THE FUTURE

    if (len(rows) > 0):
        return jsonify({'message': 'Email already exists'})
    elif (len(password) < 9):
        return jsonify({'message': 'Password must be at least 8 characters long'})
    else:
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_pw))
        return jsonify({'message': f'Verifcation email was sent to {email}'})




if __name__ == '__main__':
    app.run(debug=True)
