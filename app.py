from flask import Flask, render_template, redirect, request, url_for, session, g, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret'

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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("store.html")


@app.route("/create-account")
def create_account():
    return render_template('create-account.html')


@app.route("/submit-form", methods=['GET', 'POST'])
def authenticate():
    Username = request.form["Username"]
    Password = request.form["Password"]

    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE email = ? AND password = ?', (Username, Password))
    user = cursor.fetchone()

    if user:
        session['user_id'] = user['id']
        session['email'] = user['email']
        return redirect(url_for('store'))
    
    return redirect(url_for('login'))

    

@app.route("/submit-account", methods=["GET","POST"])
def check_account():

    data = request.get_json()

    email = data.get("New_Email")
    password = data.get("New_Password")

    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        return jsonify({'message': 'Email already exists'})
    if not password or len(password) < 9:
        return jsonify({'message': 'Password must be at least 8 characters long'})

    #THE CODE BELOW IS FOR TESTING PURPOUSES. WILL GET SENT A EMAIL IN THE FUTURE
    db.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
    db.commit()
    return jsonify({'message': f'Verifcation email was sent to {email}'})




if __name__ == '__main__':
    app.run(debug=True)
