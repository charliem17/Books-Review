from flask import Blueprint, render_template, session, request, redirect, url_for
from books_package import db

entry_page = Blueprint('entry_page', __name__, template_folder='templates')

@entry_page.route("/")
def enter():
    user = session.get('user')
    if user is None:
        return render_template("login.html")
    else:
        return redirect(url_for('search_page.search'))


@entry_page.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    # Check to see if username exists in db
    data = db.execute("SELECT username, password FROM users WHERE username = :username AND password = :password", 
                     {"username": username, "password": password}).fetchone()
    if data is None:
        return render_template("login.html", message="Error logging in. Please try again or create an account.")

    session["user"] = username

    return redirect(url_for('search_page.search'))


@entry_page.route("/signup")
def signup_page():
    return render_template("signup.html")


@entry_page.route("/signup", methods=["POST"])
def signup():

    username = request.form.get("username")
    password = request.form.get("password")

    if len(username) < 4:
        return render_template("signup.html", message="Please enter a username that is greater than 4 characters.")

    if len(password) < 4:
        return render_template("signup.html", message="Please enter a password that is greater than 4 characters.")

    username_data = db.execute("SELECT username FROM users WHERE username = :username",
                              {"username": username}).fetchone()
    if username_data is not None:
        return render_template("signup.html", message="Username is already in use. Please pick a different one.")

    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
              {"username": username, "password": password})
    db.commit()

    return render_template("login.html", message="Account created successfully! You may now login.")
