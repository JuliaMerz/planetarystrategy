from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import Required, Length
from app.models import User
from werkzeug.security import check_password_hash

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

    def validate(self):
        user = User.query.filter_by(username = self.username.data).first()
        if user is None:
            self.username.errors.append('Username does not exist')
            return False
        if not check_password_hash(user.password, self.password.data):
            self.password.errors.append('Username and password do not match')
            return False
        return True

class RegisterForm(Form):
    username = TextField('username', validators = [Required(), Length(min=3, max=40)])
    password = PasswordField('password', validators = [Required()])
    confirm_password = PasswordField('confirm_password', validators = [Required()])
    email = TextField('email', validators = [Required(), Length(max=80)])
    confirm_email = TextField('confirm_email', validators = [Required(), Length(max=80)])

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(username = self.username.data).first()
        if user is not None:
            self.username.errors.append('Username already in use. Please choose a different one.')
            return False
        if self.password.data != self.confirm_password.data:
            self.password.errors.append('Passwords must match!')
            return False
        if self.email.data != self.confirm_email.data:
            self.email.errors.append('Emails must match!')
            return False
        return True

class PostArticle(Form):
    content = TextAreaField('content', validators = [Required()])
    machine_name = TextField('machine_name', validators = [Required(), Length(max=30)])
    description = TextAreaField('description', validators = [Required(), Length(max=1000)])
    category = TextField('category', validators =[Required(), Length(max=30)])
    title = TextField('title', validators = [Required(), Length(max=120)])
