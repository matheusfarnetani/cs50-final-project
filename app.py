from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from helpers import login_required

app = Flask(__name__)


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
    ...


@app.route("/login")
def login():
    ...


@app.route("/register")
def register():
    ...


# Change flask config if started with 'py' or 'python'
if __name__ == "__main__":
    app.run(debug=True, port=3000)
