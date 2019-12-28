from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, CreatePostForm
from app.forms import RegisterForm
from app.models import User, is_admin, Post


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',
                           title='Home',
                           is_admin=is_admin())


@app.route('/dashboard')
@login_required
def dashboard():
    if not is_admin():
        flash('You are not administrator', 'danger')
        return redirect('index')
    return render_template('dashboard/index.html',
                           title='Dashboard')


@app.route('/dashboard/users')
@login_required
def dashboard_users():
    user = User.query.all()
    return render_template('dashboard/user_all.html',
                           title="All Users",
                           user=user,
                           len=len(user))


@app.route('/dashboard/post/new', methods=['GET', 'POST'])
@login_required
def dashboard_post_new():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.content = form.content.data
        post.user_id = current_user.id
        db.session.add(post)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('dashboard/post_new.html',
                           title="New Post",
                           form=form)


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    title = 'Profile - ' + user.username
    return render_template('profile.html',
                           user=user,
                           title=title,
                           is_admin=is_admin())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'warning')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in', 'warning')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect('login')
    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
