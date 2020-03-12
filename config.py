import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=900)
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY') or 'has no key'
    MAILGUN_API_DOMAIN = os.environ.get('MAILGUN_API_DOMAIN') or 'has no domain'
    MAILGUN_EMAIL_SENDER = os.environ.get('MAILGUN_EMAIL_SENDER') or 'has no email'