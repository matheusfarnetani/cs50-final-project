from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from flask_login import login_user, current_user, logout_user

from ...database.models import Users, Cards
from ...extensions import db, bcrypt, login_manager
from .forms import Register_form, Login_form

# Blueprint Variable
common_bp = Blueprint("common", __name__, url_prefix="/common")


@common_bp.route("/")
def index():
    return redirect(url_for("common.login"))


@common_bp.route("/login", methods=["GET", "POST"])
def login():

    # Get form with WTForms
    form = Login_form(request.form)

    if request.method == "POST" and form.validate_on_submit():
        # Get data from form
        username = form.username.data
        password = form.password.data

        user_record = Users.query.filter_by(username=username).first()
        if not user_record or not bcrypt.check_password_hash(user_record.password, password):
            flash("Invalid Username or password!", "danger")
            return redirect(url_for('login'))

        login_user(user_record)

        if current_user.is_authenticated:
            session["user_type"] = user_record.type
            session["user_card_id"] = user_record.card_id
            return redirect(url_for("auth.index"))

    return render_template("login.html", form=form)


@common_bp.route('/logout')
# @login_required
def logout():

    db.session.close()
    session.clear()
    logout_user()

    return redirect(url_for("common.index"))


@common_bp.route('/register', methods=['GET', 'POST'])
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
        card_record = Cards.query.filter_by(uid=form.card.data).first()
        card_uid = card_record.id

        # Update 'has_user'
        card_record.has_user = 1

        # Create a new user
        new_user = Users(username=username, email=email, password=bcrypt.generate_password_hash(
            password), type=user_type, card_id=card_uid)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('common.login'))

    return render_template('register.html', form=form)