from app import db

ROLE_USER = 0
ROLE_WRITER = 1
ROLE_MODERATOR = 2
ROLE_ADMIN = 3


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40), index = True, unique = True)
    email = db.Column(db.String(80), index = True, unique = True)
    password = db.Column(db.String(66))
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    registered = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(1000))
    body = db.Column(db.Text)
    category = db.Column(db.String(30), index = True)
    machine_name = db.Column(db.String(30), index= True)
    type = db.Column(db.String(30), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % (self.body)

