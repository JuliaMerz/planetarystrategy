from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, lm
from flask.ext.login import current_user, login_user, login_required, logout_user
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash
from datetime import datetime
from models import User, Post

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", 
            title = "Home")

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/article/<article>')
def article(articleid):
    article = Post.query.get(articleid)
    if not article:
        abort(404)
    return render_template('articlepage.html',
            article = article)
    

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if not login_user(User.query.filter_by(username = form.username.data).first(), form.remember_me.data):
            flash('Error logging in')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html',
        title = 'Login',
        form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email=form.email.data, password=generate_password_hash(form.password.data), registered=datetime.utcnow(), last_seen=datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html',
        title='Register',
        form = form)
