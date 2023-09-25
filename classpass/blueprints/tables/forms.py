from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TimeField

class SearchTable(FlaskForm):
    card = StringField('card', render_kw={"placeholder": "Search by card"})
    type = SelectField('User type', choices=[
        ('all', 'All'),
        ('student', 'Student'),
        ('collaborator', 'Collaborator'),
        ('visitant', 'visitant')])
    date = DateField('Date')
    time = TimeField('Time')