from flask import Blueprint, render_template, session, redirect, url_for, request
from books_package import db
import requests

book_page = Blueprint("book_page", __name__, template_folder="templates", url_prefix="/book")

KEY = "AIzaSyAFCoHgSfQxQKXKjdOoCYUMkUgITNoveUE"

class Book:
    def __init__(self, isbn, title, authors, rating, numberOfRatings, fromAPI):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.rating = rating
        self.numberOfRatings = numberOfRatings
        self.fromAPI = fromAPI

@book_page.route("/<isbn>")
def book(isbn):

    if isbn is "":
        return "No isbn value entered"

    user = session.get("user")
    if user is None:
        return redirect(url_for("entry_page.enter"))

    # Google Books API Get Request
    api_response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={KEY}").json()
    book = None
    try:
        for i in range(0, len(api_response['items'])):
            try:
                title = api_response['items'][i]['volumeInfo']['title']

                # Possibility of >= 1 author(s)
                authors_data = api_response['items'][i]['volumeInfo']['authors']
                authors = ''
                for i in range(0, len(authors_data)):
                    authors += authors_data[i]

                rating = api_response['items'][i]['volumeInfo']['averageRating']
                numberOfRatings = api_response['items'][i]['volumeInfo']['ratingsCount']

                book = Book(isbn=isbn, title=title, authors=authors, rating=rating, numberOfRatings=numberOfRatings, fromAPI=True)

            except:
                # Do nothing
                print('Error in books_page routes.py')
    except:
        print('Error in books_page routes.py for loop')
    
    # Get all reviews from our website database
    db_response = db.execute("SELECT username, rating, review, date FROM reviews WHERE isbn = :isbn", 
                             {"isbn": isbn}).fetchall()

    # If Google had no data, pull from our own
    if book is None:
        db_book = db.execute("SELECT title, author FROM books WHERE isbn = :isbn", 
                            {"isbn": isbn}).fetchone()
        print(db_book.author)

        book = Book(isbn=isbn, title=db_book.title, authors=db_book.author, rating=None, numberOfRatings=None, fromAPI=False)

    return render_template("book.html", book=book, reviews=db_response)

@book_page.route("/")
def null_book():

    user = session.get("user")
    if user is None:
        return redirect(url_for("entry_page.enter"))

    return "No book value to search for."

@book_page.route("/", methods=['POST'])
def review_book():

    user_input = request.form.get("input")
    user_rating = int(request.form.get("rating"))
    isbn = request.form.get("isbn")
    user = session.get("user")
    print(f"{user} updating {isbn}")

    # Check if user has already made review
    response = db.execute("SELECT * FROM reviews WHERE username = :user AND isbn = :isbn",
                          {"user": session.get("user"), "isbn": isbn}).fetchone()

    if response != None:
        # Update the review
        db.execute("UPDATE reviews SET rating = :rating, review = :review, date = DEFAULT WHERE username = :user AND isbn = :isbn",
                    {"rating": user_rating, "review": user_input, "user": session.get("user"), "isbn": isbn})
    else:
        # Submit data to db
        db.execute("INSERT INTO reviews (username, rating, review, isbn) VALUES(:username, :rating, :review, :isbn)",
                    {"username": session.get("user"), "review": user_input, "rating": user_rating, "isbn": isbn})

    db.commit()

    return redirect(url_for('book_page.book', isbn=isbn))
