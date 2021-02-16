from flask import render_template, url_for, flash,redirect, request
from wtforms.validators import Email
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author':'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20,2018'
    },
    {
        'author':'Siddharth Mehta',
        'title': 'Blog Post 2',
        'content': 'second post content',
        'date_posted': 'April 21,2018'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return "<h1> Home Page</h1>"
    # return render_template('home.html', posts=posts )


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashedPass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        print("User added to database: {}".format(User.query.filter_by(username="Siddharth").first()))
        redirect(url_for("login"))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        passwordCheck = bcrypt.check_password_hash(user.password, form.password.data)
        if user and passwordCheck:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")
            print("wrong credentials")

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required #cant access the page without loggin in
def account():
    return render_template('account.html', title='Account')