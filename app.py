from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required
from helpersdb import query_username, create_new_user, get_by_username, get_locals, search_tables
from forms import RegistrationForm, LoginForm, SearchTable

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


@app.route('/graphs')
@login_required
def graph():

    return render_template('graphs.html')


@app.route("/login", methods=["GET", "POST"])
def login():

    # Clean session
    session.clear()

    # Get form with WTForms
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():

        # Get data from database
        user_data = get_by_username(form.username.data)
        if user_data == None:
            return redirect("/login")

        # Ensure password is correct
        if not check_password_hash(user_data["hash"], form.password.data):
            return render_template("login.html", form=form)

        # Store user's id
        session["user_id"] = user_data["id"]

        # Redirect to main page
        return redirect("/")

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():

    session.clear()

    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():

    # Get form with WTForms
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():

        # Create dict
        newUser = {'username': form.username.data,
                   'email': form.email.data,
                   'hash': generate_password_hash(form.password.data),
                   'type': form.type.data,
                   'card': form.card.data}

        # Register
        resultRegister = create_new_user(newUser)
        if not resultRegister:
            return render_template('register.html')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/tables')
@login_required
def tables():

    # Create WTForm
    form = SearchTable(request.form)

    rows_local = get_locals()
    if not rows_local:
        return redirect('/tables')

    return render_template('tables.html', form=form, local_bt=rows_local)


@app.route('/tables/search')
@login_required
def tablesSearch():

    # Creating 'route's args'
    argsCard = request.args.get('card')
    argsDate = request.args.get('date')
    argsTime = request.args.get('time')
    argsType = request.args.get('type')
    argsLocal = request.args.get('local')

    results = search_tables(card=argsCard, date=argsDate, time=argsTime, card_type=argsType, local=argsLocal)

    return jsonify(results)


# Change flask config when using 'python app.py'
if __name__ == "__main__":
    app.run(debug=True, port=3000)
