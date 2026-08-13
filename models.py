import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

basedir = os.path.abspath(os.path.dirname(__file__))

# Create database connection
engine = create_engine(f"sqlite:///{os.path.join(basedir, 'data/movies_app.db')}")

# Create session factory
Session = sessionmaker(bind=engine)

# Data table class's parent class
Base = declarative_base()

# Users table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name}"


# Movies table
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    director = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    poster_url = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return (f"Movie(id = {self.id}, title = {self.title}, director = {self.director}, "
                f"year = {self.year}, poster_url = {self.poster_url}")

