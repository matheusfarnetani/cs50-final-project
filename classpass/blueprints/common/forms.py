from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, EmailField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp
from wtforms import ValidationError
from sqlalchemy.orm import validates

from ...extensions import bcrypt
from ...database.models import Users, Cards, Type


class Register_form(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])

    email = EmailField('Email Address', validators=[InputRequired(), Email(
        message="Invalid email format")])

    password = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=72), EqualTo('confirm', message='Passwords must match'), Regexp(
        r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message='Password must contain at least one uppercase letter, one digit, and one special character from @$!%*?&')])

    confirm = PasswordField('Repeat Password', validators=[InputRequired()])

    type = SelectField('User type', choices=[('student', 'student'), ('collaborator', 'collaborator'), ('visitant', 'visitant')])

    card = StringField('Card UID', validators=[Length(min=11, max=11)])

    # Validation on Client-Side
    def validate_email(self, email):
        if Users.query.filter_by(email=self.email.data).first():
            raise ValidationError("Email already registered!")

    def validate_username(self, username):
        if Users.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username already taken!")
        
    @validates('type')
    def validate_card(self, card):
        card_record = Cards.query.filter_by(uid=self.card.data).first()
        if not card_record:
            raise ValidationError("Card not found!")

        if card_record.has_user == 1:
            raise ValidationError("Card already in use!")

        if card_record.type != Type(self.type.data):
            raise ValidationError("Card type does not match selected user type!")



class Login_form(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=72)])
    
    def validate_username(self, username):
        if not Users.query.filter_by(username=self.username.data).first():
            raise ValidationError("Username does not exist!")

    def validate_password(self, password):
        user_record = Users.query.filter_by(username=self.username.data).first()
        if user_record and not bcrypt.check_password_hash(user_record.password, self.password.data):
            raise ValidationError("Password is not valid!")
