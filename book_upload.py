import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

USERNAME = "postgres"
PASSWORD = "chickenpizza"
DATABASE = "project1"

engine = create_engine(f"postgres://{USERNAME}:{PASSWORD}@localhost:5432/{DATABASE}")
db = scoped_session(sessionmaker(bind=engine))

def main():
    file = open("books.csv")
    reader = csv.reader(file)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()


# if __name__ == "__main__":
#     main()

# Be sure to created two other tables:
# all are NOT NULL unless specified
# users table: user_id SERIAL PRIMARY KEY, username VARCHAR(50), password VARCHAR(50)
# reviews table: review_id SERIAL PRIMARY KEY, username VARCHAR(50), rating SMALLINT, review TEXT NULL, date DATE, isbn VARCHAR(12)