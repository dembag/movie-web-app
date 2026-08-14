from flask import jsonify
from sqlalchemy import select, delete
from models import Session, Movie, User


class DataManager:
    """ Contains methods for CRUD operations on the database."""

    def __init__(self):
        self.session = Session()

    def create_user(self, name):
        new_user = User(name=name)
        self.session.add(new_user)
        self.session.commit()
        return new_user


    def get_users(self):
        """ Returns a list of all users."""
        query = select(User).order_by(User.name.asc())
        all_users = self.session.execute(query).scalars().all()
        return all_users


    def get_user_by_id(self, user_id):
        """ Returns a single user by id."""
        query = select(User).where(User.id == user_id)
        user = self.session.execute(query).scalar_one_or_none()
        return user


    def get_movies(self, user_id):
        """ Returns a list of movies for a specific user."""
        query = select(Movie).where(Movie.user_id == user_id).order_by(Movie.title)
        user_movies = self.session.execute(query).scalars().all()
        return user_movies


    def add_movie(self, new_movie):
        """ Receives a Movie object and adds it to a users favourites."""
        try:
            self.session.add(new_movie)
            self.session.commit()
            return new_movie
        except Exception:
            self.session.rollback()
            raise


    def update_movie(self, movie_id, new_title):
        """ Updates the details of a specific movie in the database."""
        query = select(Movie).where(Movie.id == movie_id)
        movie_to_update = self.session.execute(query).scalar_one()
        movie_to_update.title = new_title
        self.session.commit()
        return movie_to_update


    def delete_movie(self, movie_id):
        """ Deletes the movie from the users list of favourites."""
        query = delete(Movie).where(Movie.id == movie_id)
        self.session.execute(query)
        self.session.commit()
        return "Movie successfully deleted."