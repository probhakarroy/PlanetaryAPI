import os


class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'random string from xkcd password generator.'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///planets.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')