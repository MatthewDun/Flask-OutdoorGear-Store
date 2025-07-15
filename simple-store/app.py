from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])

def home():
    return render_template("login.html")


@app.route("/store")

def store():
    return render_template("store.html")


@app.route("/submit-form", methods=["GET", "POST"])

def authenticate():
    Username = request.form["Username"]
    Password = request.form["Password"]

    print("Username is", Username)
    if Username == "Admin" and Password == "Pass":
        return redirect(url_for('store'))
    else:
        return redirect(url_for('home'))
    







if __name__ == '__main__':
    app.run(debug=True)
