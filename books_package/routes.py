from flask import render_template, request, session
from books_package import app, db

from books_package.blueprints.entry_page.routes import entry_page
from books_package.blueprints.search_page.routes import search_page
from books_package.blueprints.profile_page.routes import profile_page
from books_package.blueprints.book_page.routes import book_page
from books_package.blueprints.api.routes import api_page

app.secret_key = "alsiewn54o231k" # Can be anything

app.register_blueprint(entry_page)
app.register_blueprint(search_page)
app.register_blueprint(profile_page)
app.register_blueprint(book_page)
app.register_blueprint(api_page)

# Here would be @app.route(""), but we currently have none
# We are using blueprints