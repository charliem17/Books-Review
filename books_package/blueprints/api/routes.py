from flask import Blueprint, jsonify
from books_package import db

api_page = Blueprint("api", __name__, url_prefix="/api")

@api_page.route("/<isbn>")
def isbn_repsonse(isbn):
    
    book_data = db.execute("SELECT title, author, year FROM books WHERE books.isbn = :isbn",
                          {"isbn": isbn}).fetchone()
    review_count = db.execute("SELECT COUNT(rating) FROM reviews WHERE isbn = :isbn",
                                {"isbn": isbn}).fetchone()
    review_avg = db.execute("SELECT ROUND(AVG(rating),1) FROM reviews WHERE isbn = :isbn",
                            {"isbn": isbn}).fetchone()

    return jsonify({
        "title": book_data.title,
        "author": book_data.author,
        "year": book_data.year,
        "isbn": isbn,
        "review_count": review_count[0],
        "average_score": str(review_avg[0])
    })