from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required
from helpersdb import query_username, create_new_user, get_by_username
from hlpwtforms import RegistrationForm, LoginForm

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

    # Get form with WTForms
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():

        # Get data from database
        user_data = get_by_username(form.username.data)

        # Ensure password is correct
        if not check_password_hash(user_data["hash"], form.password.data):
            return render_template("login.html", form=form)

        # Store user's id
        session["user_id"] = user_data["id"]

        # Redirect to main page
        return redirect("/")

    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    # Get form with WTForms
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():

        # Create dict
        newUser = {'username': form.username.data,
                   'email': form.email.data,
                   'hash': generate_password_hash(form.password.data),
                   'type': form.type.data}

        # Register
        resultRegister = create_new_user(newUser)
        if not resultRegister:
            return render_template('register.html')

        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


# Change flask config when using 'python app.py'
if __name__ == "__main__":
    app.run(debug=True, port=3000)
