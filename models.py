from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Users table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


# Movies table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)