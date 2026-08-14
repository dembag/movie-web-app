import os
from flask import Flask, jsonify, render_template, redirect, request
from data_manager import DataManager
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
    users = dm.get_users()
    print(users)
    user = dm.get_user_by_id(user_id)
    if user is None:
        return jsonify({
            "error": "User not found!"
        }), 404

    movie_list = dm.get_movies(user_id)
    return render_template("movies.html", user=user.name, movies=movie_list)







if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)