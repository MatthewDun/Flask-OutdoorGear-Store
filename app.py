from flask import Flask, render_template, redirect, request, url_for, session, abort

app = Flask(__name__)
app.secret_key = 'secret'


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
    


if __name__ == '__main__':
    app.run(debug=True)
