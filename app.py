import os
from flask import Flask, render_template
from data_manager import DataManager
from models import Base, engine, Movie

app = Flask(__name__)
dm = DataManager()

@app.route("/")
def index():
    users = dm.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    users = dm.get_users()
    return str(users)               # Temporarily return users as a string


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)