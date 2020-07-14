import os


class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'shoot will allow rock'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///planets.db'
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')