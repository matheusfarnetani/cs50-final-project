from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from helpers import login_required
from helpersdb import query_username

app = Flask(__name__)

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
    return redirect("/login")


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
            print("user_data = None")
        else:
            print(user_data)

        # Store user's id
        # session["user_id"] = rows[0]["id"]

    return render_template("login.html")


@app.route("/register")
def register():
    ...


# Change flask config if started with 'py' or 'python'
if __name__ == "__main__":
    app.run(debug=True, port=3000)
