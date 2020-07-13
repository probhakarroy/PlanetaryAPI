import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shoot will allow rock'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///planets.db'