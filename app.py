import os
from dotenv import load_dotenv
import requests
from flask import Flask, jsonify, render_template, redirect, request


from data_manager import DataManager
import data_manager
from models import Base, engine, Movie

app = Flask(__name__)
dm = DataManager()


@app.route("/")
def index():
    users = dm.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_users():
    """ Gets new_user_name from the form and adds the new user to users table."""
    users = dm.get_users()

    new_user_name = request.form["new_user_name"].strip()

    # Validate data
    if not new_user_name:
        return jsonify({
            "error": "Name is required."
        }), 400

    # Add to database
    dm.create_user(new_user_name)

    users = dm.get_users()
    return redirect("/")              # Temporarily return users as a string


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def get_movies(user_id):
    """ Displays the list of favourite movies of a specific user."""
    user = dm.get_user_by_id(user_id)
    if user is None:
        return jsonify({
            "error": "User not found!"
        }), 404

    movie_list = dm.get_movies(user.id)
    return render_template("movies.html", user=user, movies=movie_list)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_to_favourites(user_id):
    """ Adds a movie to the users favourites list."""
    user = dm.get_user_by_id(user_id)
    new_movie_title = request.form.get("title")
    new_movie_year = request.form.get("year")

    new_movie_year = int(new_movie_year) if new_movie_year else None

    # Get movie data from API
    new_movie_data = data_manager.fetch_movie_from_omdb(new_movie_title, new_movie_year)

    if not new_movie_data:
        # OMDB found nothing --------------------rerender with error handling
        return render_template("movies.html", user_id=user_id, user=user, movies=movies,
                               error="Movie not found")

    # Format data for movies table
    new_movie = Movie(
        title=new_movie_data.get("Title"),
        director=new_movie_data.get("Director"),
        year=new_movie_data.get("Year"),
        poster_url=new_movie_data.get("Poster"),
        user_id=user_id
    )

    added_movie = dm.add_movie(new_movie)

    movies = dm.get_movies(user_id)
    print(new_movie_data)

    return render_template("movies.html", user_id=user_id, user=user, movies=movies)




if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)