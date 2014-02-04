from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db, lm
from flask.ext.login import current_user, login_user, login_required, logout_user
from forms import LoginForm, RegisterForm, PostArticle
from werkzeug.security import generate_password_hash
from datetime import datetime
from models import User, Post, ROLE_WRITER

@app.route('/')
@app.route('/index')
def index():
    query = Post.query.order_by(Post.timestamp.desc())
    articles = query.paginate(1, 4, False).items
    return render_template("index.html", 
            title = "Home",
            articles=articles)
'''
@app.route('/get-article/<id>')
def get_article(id):
    article = Post.query.get(id)
    return render_template("article-inner.html",
            article=article)

@app.route('/get-article-preview/<id>')
def get_article_preview(id):
    article = Post.query.get(id)
    return render_template("articlepreview-inner.html",
            article=article)
'''

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

@app.route('/article/<articleid>')
def article(articleid):
    article = Post.query.get(articleid)
    if not article:
        abort(404)
    return render_template('article_page.html',
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

@app.route('/post-article', methods = ['GET', 'POST'])
def post_article():
    if g.user is None or not g.user.is_authenticated() or g.user.role < ROLE_WRITER:
      return redirect(url_for('index'))
    form = PostArticle()
    if form.validate_on_submit():
        article = Post(body = form.content.data, title=form.title.data, description=form.description.data, category=form.category.data, machine_name=form.machine_name.data, author=g.user, type="article", timestamp = datetime.utcnow())
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post_article.html',
        title='Post Article',
        form = form)
