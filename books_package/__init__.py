from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

USERNAME = "postgres"
PASSWORD = "chickenpizza"
DATABASE = "project1"

engine = create_engine(f"postgres://{USERNAME}:{PASSWORD}@localhost:5432/{DATABASE}")
db = scoped_session(sessionmaker(bind=engine))

from books_package import routes # routes imports 'app' and 'db'