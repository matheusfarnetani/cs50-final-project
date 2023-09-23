from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from forms import Register_form, Login_form, SearchTable
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from datetime import date
from sqlalchemy import select, ScalarSelect

import database.models as models
from app import create_app, db, login_manager, bcrypt
from graphs import people_by_type, equipments_by_place, registers_by_place, place_user


@login_manager.user_loader
def load_user(user_id):
    return models.Users.query.get(int(user_id))


app = create_app()


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
    # TODO - Display users info
    return render_template("overview.html")


@app.route("/graphs/", defaults={'graph_id': 1})
@app.route("/graphs/<int:graph_id>")
@login_required
def graph(graph_id):

    data = people_by_type()

    return render_template("graphs.html", data=data)


@app.route("/graphs/<int:graph_id>/data")
def graphsData(graph_id):
    if graph_id == 1:
        data = people_by_type()
    elif graph_id == 2:
        data = equipments_by_place()
    elif graph_id == 3:
        data = registers_by_place()
    elif graph_id == 4:
        argsPlace = request.args.get("place")
        if not argsPlace:
            argsPlace = "entrance 01"
        data = place_user(argsPlace)
    else:
        return jsonify(None)

    return jsonify(data)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Get form with WTForms
    form = Login_form(request.form)

    if request.method == "POST" and form.validate_on_submit():
        # Get data from form
        username = form.username.data
        password = form.password.data

        user_record = models.Users.query.filter_by(username=username).first()
        if not user_record or not bcrypt.check_password_hash(user_record.password, password):
            flash("Invalid Username or password!", "danger")
            return redirect(url_for('login'))

        login_user(user_record)

        if current_user.is_authenticated:
            session["user_type"] = user_record.type
            session["user_card_id"] = user_record.card_id
            return redirect("/")

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():

    db.session.close()
    session.clear()
    logout_user()

    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():

    # Get form with WTForms
    form = Register_form(request.form)

    if request.method == 'POST' and form.validate_on_submit():

        # Get data from form
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user_type = form.type.data

        # Get data from Cards
        card_record = models.Cards.query.filter_by(uid=form.card.data).first()
        card_uid = card_record.id

        # Update 'has_user'
        card_record.has_user = 1

        # Create a new user
        new_user = models.Users(username=username, email=email, password=bcrypt.generate_password_hash(
            password), type=user_type, card_id=card_uid)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/tables')
@login_required
def tables():

    # Create WTForm
    form = SearchTable(request.form)

    places = models.Places.query.all()
    for place in places:
        print(place)

    return render_template('tables.html', form=form, places=places)


@app.route('/tables/search')
@login_required
def tablesSearch():

    # Creating "route's args"
    argsCard = request.args.get('card')
    argsDate = request.args.get('date')
    argsTime = request.args.get('time')
    argsType = request.args.get('type')
    argsPlace = request.args.get('place')

    # Base SQLAlchemy query
    query = db.session.query(
        models.Cards.type.label('card type'),
        models.Cards.uid.label('card uid'),
        models.Registers.date,
        models.Registers.hour,
        models.Registers.minute,
        models.Registers.second,
        models.Equipments.description.label('equipment'),
        models.Places.description.label('place')
    )

    # Joining tables with explicit join conditions
    query = query.join(models.Registers, models.Cards.id ==
                       models.Registers.card_id)
    query = query.join(models.Equipments,
                       models.Registers.equipment_id == models.Equipments.id)
    query = query.join(
        models.Places, models.Equipments.place_id == models.Places.id)

    # Add conditions based on user input
    if argsCard:
        query = query.filter(models.Cards.uid.like(f"%{argsCard}%"))
    if argsDate:
        query = query.filter(models.Registers.date == argsDate)
    if argsTime:
        query = query.filter(
            models.Registers.hour == argsTime.hour,
            models.Registers.minute == argsTime.minute,
            models.Registers.second == argsTime.second
        )
    if argsType:
        query = query.filter(models.Cards.type == argsType)
    if argsPlace:
        query = query.filter(models.Places.description == argsPlace)

    # Add ORDER BY clause
    query = query.order_by(
        models.Registers.date.desc(),
        models.Registers.hour.desc(),
        models.Registers.minute.desc(),
        models.Registers.second.desc()
    )

    query = query.limit(50)

    # Execute the query and fetch the results as a list of dictionaries
    results = []
    for row in query.all():
        result_dict = {
            'card type': row[0].value,
            'card uid': row[1],
            'date': row[2].strftime('%d/%m/%Y'),
            'hour': str(row[3]),
            'minute': str(row[4]),
            'second': str(row[5]),
            'equipment': row[6],
            'place': row[7]
        }
        results.append(result_dict)

    return jsonify(results)


@app.route("/user/data")
@login_required
def user_data():
    # TODO
    # Remake query with joins 
    registers_query = db.session.query(models.Registers).filter_by(
        card_id=session["user_card_id"]).all()
    
    registers = [register.as_dict() for register in registers_query]

    for item in registers:
        print(item)

    return jsonify(registers)


# Change flask config when using 'python routes.py'
if __name__ == "__main__":
    app.run(debug=True, port=3000)
