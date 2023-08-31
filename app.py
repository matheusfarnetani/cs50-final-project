from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required
from helpersdb import query_username

app = Flask(__name__)

# TODO - Create env var
app.secret_key = "debug123"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def overview():
    return render_template("overview.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Clean session
    session.clear()

    if request.method == "POST":

        # Ensure username and password was submitted
        inputtedUsername = request.form.get("username")
        if not inputtedUsername:
            flash("No username was received.")
            return redirect("/login")
        inputtedPassword = request.form.get("password")
        if not inputtedPassword:
            flash("No password was received..")
            return redirect("/login")

        print(inputtedUsername, inputtedPassword)

        # Query database for username
        user_data = query_username(inputtedUsername)
        if user_data == None:
            return render_template("login.html", usernameError=True)
        
        print(user_data)
        print(user_data["id"], user_data["username"], user_data["hash"], user_data["cash"])

        # Ensure password is correct
        if not check_password_hash(user_data["hash"], inputtedPassword):
            return render_template("login.html", passwordError=True)

        # Store user's id
        session["user_id"] = user_data["id"]

        # Redirect to main page
        return redirect("/")

    return render_template("login.html")


@app.route("/register")
def register():
    ...


# Change flask config when using 'python app.py'
if __name__ == "__main__":
    app.run(debug=True, port=3000)
