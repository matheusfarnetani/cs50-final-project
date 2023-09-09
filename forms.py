from wtforms import Form, BooleanField, StringField, PasswordField, EmailField, SelectField, DateField, TimeField, validators
from helpersdb import check_username, check_card_uid
import re


def validateUsernameAvailability(form, field):
    if not check_username(field.data):
        raise validators.ValidationError(message="Username is not available.")


def validateUsernameExistence(form, field):
    if check_username(field.data):
        raise validators.ValidationError(message="Username doesn't exist.")


# Currently using Regexp instead of validatePassword
def validatePassword(form, field):
    """Check if password has letter, number and symbol."""
    password = field.data
    if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", password):
        raise validators.ValidationError(
            "Password must contain: 1 lowercase; 1 uppercase; 1 digit; and 1 symbol")


# Validate card UID
def validateCardUid(form, field):
    """Check if Card UID exists in the database"""
    cardUid = check_card_uid(field.data, form.type.data)
    if not cardUid:
        raise validators.ValidationError("Invalid card UID.")


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(
        min=4, max=15), validateUsernameAvailability], render_kw={"placeholder": "username"})
    email = EmailField('Email Address', [validators.Email(
        message="Invalid email format")], render_kw={"placeholder": "email@app.com"})
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match'), validators.Regexp(
        r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message='Password must contain at least one uppercase letter, one digit, and one special character from @$!%*?&')], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', render_kw={
                            "placeholder": "Confirm Password"})
    type = SelectField('User type', choices=[
        ('student', 'student'),
        ('collaborator', 'collaborator'),
        ('visitor', 'visitor')
    ])
    card = StringField('Card UID', [validators.Length(
        min=11, max=11), validateCardUid], render_kw={"placeholder": "card UID"})


class LoginForm(Form):
    username = StringField(
        'Username', [validators.DataRequired(), validateUsernameExistence])
    password = PasswordField('Password', [validators.DataRequired()])


class SearchTable(Form):
    card = StringField('card', [validateCardUid], render_kw={
                       "placeholder": "Search by card"})
    type = SelectField('User type', choices=[
        ('all', 'All'),
        ('student', 'Student'),
        ('collaborator', 'Collaborator'),
        ('visitor', 'Visitor')])
    date = DateField('Date')
    time = TimeField('Time')
