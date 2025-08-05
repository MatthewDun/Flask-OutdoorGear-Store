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
    if not session.pop('from-login', False):
        return redirect(url_for('login'))
    return render_template("store.html")



@app.route("/create-account")

def create_account():
    return render_template('create-account.html')

def check_account():
    New_Email = request.form["New_Email"]
    New_Password = request.form["New_Password"]

    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE email = ?', (New_Email,))
    rows = cursor.fetchall()

    balls = "walls"

    if (len(rows) > 0):
        balls = "balls"

    return f"<h1>{balls} is what is is</h1>"





@app.route("/submit-form", methods=["GET", "POST"])

def authenticate():
    Username = request.form["Username"]
    Password = request.form["Password"]

    print("Username is", Username)
    if Username == "Admin" and Password == "Pass":
        session['from-login'] = True
        return redirect(url_for('store'))
    else:
        return redirect(url_for('login'))

    #return f"<h1>Id {results[0]['id']}. <br> Email {results[0]['email']} <br> Password {results[0]['password']} <br>"

    
    
@app.route("/submit-account", methods=["GET","POST"])

def check_account():

    data = request.get_json()

    email = data.get("New_Email")


    db = get_db()
    cursor = db.execute('SELECT * FROM users WHERE email = ?', (email,))
    rows = cursor.fetchall()

    if (len(rows) > 0):
        return jsonify({'message': 'Email already exists'})
    else:
        return jsonify({'message': f'Verifcation email was sent to {email}'})
        




if __name__ == '__main__':
    app.run(debug=True)
