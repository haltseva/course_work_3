import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://ka7603:Sveta1976@zanner.org.ua:33321/ka7603'
    SQLALCHEMY_TRACK_MODIFICATIONS = False