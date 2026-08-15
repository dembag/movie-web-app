import os
from dotenv import load_dotenv
import requests
from sqlalchemy import select, delete
from models import Session, Movie, User

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

class DataManager:
    """ Contains methods for CRUD operations on the database."""

    def create_user(self, name):
        with Session() as session:
            new_user = User(name=name)
            session.add(new_user)
            session.commit()
            return new_user


    def get_users(self):
        """ Returns a list of all users."""
        with Session() as session:
            query = select(User).order_by(User.name.asc())
            all_users = session.execute(query).scalars().all()
            return all_users


    def get_user_by_id(self, user_id):
        """ Returns a single user by id."""
        with Session() as session:
            query = select(User).where(User.id == user_id)
            user = session.execute(query).scalar_one_or_none()
            return user


    def get_movies(self, user_id):
        """ Returns a list of movies for a specific user."""
        with Session() as session:
            query = select(Movie).where(Movie.user_id == user_id).order_by(Movie.title)
            user_movies = session.execute(query).scalars().all()
            return user_movies


    def add_movie(self, new_movie):
        """ Receives a Movie object and adds it to a users favourites."""
        with Session() as session:
            try:
                session.add(new_movie)
                session.commit()
                new_movie_title = new_movie.title
                return new_movie_title
            except Exception:
                session.rollback()
                raise


    def update_movie(self, user_id, movie_id, new_title):
        """ Updates the title of a specific movie for a specific user in the database."""
        with Session() as session:
            query = select(Movie).where(
                Movie.id == movie_id,
                Movie.user_id == user_id
            )
            movie_to_update = session.execute(query).scalar_one()
            movie_to_update.title = new_title
            session.commit()
            return movie_to_update


    def delete_movie(self, user_id, movie_id):
        """ Deletes the movie from the users list of favourites."""
        with Session() as session:
            query = delete(Movie).where(
                Movie.id == movie_id,
                Movie.user_id == user_id
            )
            session.execute(query)
            session.commit()
            return "Movie successfully deleted."



def fetch_movie_from_omdb(title, year=None):
    """ Gets movie information from OMDB by title and year(optional).
        returns JSON object."""
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": OMDB_API_KEY,
        "t": title
    }
    if year:
        params["y"] = year

    response = requests.get(url, params=params)
    movie_data = response.json()

    if movie_data.get("Response") == "False":
        return movie_data.get("Error")

    return movie_data


