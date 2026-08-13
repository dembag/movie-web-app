import os
from flask import Flask
from data_manager import DataManager
from models import Base, engine, Movie

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to MovieWeb App!"




if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)