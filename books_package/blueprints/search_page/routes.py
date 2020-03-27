import re

from flask import render_template, session, Blueprint, redirect, url_for, request
from books_package import db

search_page = Blueprint("search_page", __name__, template_folder="templates", url_prefix="/search")

@search_page.route("/")
def search(): 
    user = session.get('user')
    if user is None:
        return redirect(url_for('entry_page.enter'))

    return render_template("search.html", user=user)

@search_page.route("/result", methods=["GET"])
def search_result():

    input = str(request.args.get("input")).lower()

    if len(input) < 1 or input is None:
        user = session.get("user")
        return render_template("search.html", user=user)

    likeInput = f"%{input}%"

    if len(input) is 4 and re.match("^[0-9]*$", input) != None:
        # Assume a year input or a possible isbn
        data = db.execute("SELECT * FROM books WHERE year LIKE :year OR isbn LIKE :isbn",
                          {"year": likeInput, "isbn": likeInput}).fetchall()
    elif re.match("^[0-9]*$", input) != None:
        # Otherwise, an isbn
        data = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn",
                          {"isbn": likeInput}).fetchall()
    else:
        # Otherwise, title or author
        data = db.execute("SELECT * FROM books WHERE lower(title) LIKE :title OR lower(author) LIKE :author",
                          {"title": likeInput, "author": likeInput}).fetchall()

    user = session.get("user")
    return render_template("search.html", user=user, books=data)
