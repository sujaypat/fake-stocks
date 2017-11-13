import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret_key'

"""
Set up db location
"""
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
