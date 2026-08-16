from flask import Flask, jsonify, render_template, redirect, request, url_for

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

    new_user_name = request.form.get("new_user_name", "").strip()

    # Validate data
    if not new_user_name or len(new_user_name) > 15:
        return render_template("index.html", users=users,
                               error="Name is required and must be 3 to 15 characters."), 400

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
    if user is None:
        return jsonify({"error": "User not found!"}), 404

    new_movie_title = request.form.get("title", "").strip()
    new_movie_year_raw = request.form.get("year", "").strip()

    if not new_movie_title:
        movies = dm.get_movies(user_id)
        return render_template("movies.html", user_id=user_id, user=user,
                               movies=movies, error="Title is required.")

    new_movie_year = None
    if new_movie_year_raw:
        if not new_movie_year_raw.isdigit():
            movies = dm.get_movies(user_id)
            return render_template("movies.html", user_id=user_id, user=user,
                               movies=movies, error="Year must be a number.")
        new_movie_year = int(new_movie_year_raw)

    # Get movie data from API
    new_movie_data = data_manager.fetch_movie_from_omdb(new_movie_title, new_movie_year)

    if not new_movie_data:
        # OMDB found nothing
        movies = dm.get_movies(user_id)
        return render_template("movies.html", user_id=user_id, user=user, movies=movies,
                               error="Movie not found")

    # Format data for movies table
    omdb_year = new_movie_data.get("Year", "")
    safe_year = int(omdb_year[:4]) if omdb_year[:4].isdigit() else None

    director = new_movie_data.get("Director")
    director = director if director and director != "N/A" else "Unknown"

    poster_url = new_movie_data.get("Poster")
    poster_url = poster_url if poster_url and poster_url != "N/A" else None

    new_movie = Movie(
        title=new_movie_data.get("Title"),
        director=director,
        year=safe_year,
        poster_url=poster_url,
        user_id=user_id
    )

    dm.add_movie(new_movie)

    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_title(user_id, movie_id):
    """ Allows the user to update the title of a movie."""
    new_title = request.form.get("title")

    if not new_title or len(new_title) > 200:
        user = dm.get_user_by_id(user_id)
        movies = dm.get_movies(user_id)
        return render_template("movies.html", user_id=user_id, user=user, movies=movies,
                               error="Title is required and must be less than 200 characters."), 400


    updated_title = dm.update_movie(user_id, movie_id, new_title)
    if updated_title is None:
        return jsonify({"error": "Movie not found."}), 404

    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    """ Allows the user to delete a movie from their favourites."""
    deleted_movie = dm.delete_movie(user_id, movie_id)
    if deleted_movie is None:
        return jsonify({"error": "Movie not found."}), 404

    return redirect(url_for("get_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html",
                           error=error,
                           back_url=request.referrer or url_for("index")), 404


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)