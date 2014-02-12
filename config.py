#WTForm Stuff
CSRF_ENABLED = True
SECRET_KEY = 'a-different-secret-key' #Sample, change this when deploying code.

#Database config.
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['sebastian@sebastianmerz.com'] #Again, change this if you fork. I don't want your emails


