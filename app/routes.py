from datetime import datetime
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, CreateAccountForm, NewWish, NewBeen
from app.models import Post, User, City, Country
from flask_login import current_user, login_user, logout_user, login_manager
from app.models import User
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
import string

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.filter_by(type=1)
    return render_template('index.html', title='Home', User=current_user, posts=posts)


@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Invalid username')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateAccountForm()
    if form.validate_on_submit():
        new_user = form.username.data
        if User.query.filter_by(username=new_user).first() is not None:
            flash('User Already Exists')
        else:
            flash("New User {} Created!".format(form.username.data))
            country = form.country.data
            country = string.capwords(country)
            if Country.query.filter_by(name=form.country.data).first() is not None:
                c = country.query.filter_by(name=form.country.data).first()
            else:
                c = Country(name=form.country.data)
                db.session.add(c)
                db.session.commit()
            u1 = User(username=form.username.data, email=form.email.data, countryID=c.id)
            u1.set_password(form.password.data)
            db.session.add(u1)
            db.session.commit()
        return redirect('/login')

    return render_template('create_user.html', title="Create User", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/beenList', methods=['GET', 'POST'])
@login_required
def beenList():
    posts = Post.query.filter_by(type=1)
    return render_template('beenList.html', title='Been List', User=current_user, posts=posts)


@app.route('/beenNew', methods=['GET', 'POST'])
@login_required
def beenNew():
    form = NewBeen()
    if form.validate_on_submit():
        type = 1
        blog = form.blog.data
        startDate = form.startDate.data
        endDate = form.endDate.data
        user=current_user.id

        country = form.country.data
        country = string.capwords(country)
        if Country.query.filter_by(name=form.country.data).first() is not None:
            c = Country.query.filter_by(name=form.country.data).first()
        else:
            c = Country(name=form.country.data)
            db.session.add(c)
            db.session.commit()
        city = form.city.data
        city = string.capwords(city)
        if City.query.filter_by(name=form.country.data).first() is not None:
            city1 = City.query.filter_by(name=form.country.data).first()
        else:
            city1 = City(name=city, countryID=c.id)
            db.session.add(city1)
            db.session.commit()

        p = Post(type=type, blog=blog, StartDate=startDate, EndDate=endDate, cityID=city1.id, userID=user)
        db.session.add(p)
        db.session.commit()
        flash('Blog Posted')
        return redirect('/beenList')

    return render_template('beenNew.html', title='New Been Post', form=form)


@app.route('/beenPost/<id>', methods=['GET', 'POST'])
@login_required
def beenPost(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('beenPost.html', title='Been Post', user=current_user, post=post)


@app.route('/wishPost/<id>', methods=['GET', 'POST'])
@login_required
def wishPost(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('wishPost.html', title='Wish Post', user=current_user, post=post)


@app.route('/wishList', methods=['GET', 'POST'])
@login_required
def wishList():
    posts = Post.query.filter_by(type=2)
    return render_template('wishList.html', title='Wish List', User=current_user, post=posts)


@app.route('/wishNew', methods=['GET', 'POST'])
@login_required
def wishNew():
    form = NewWish()
    if form.validate_on_submit():
        type = 2
        blog = form.blog.data
        startDate = form.startDate.data
        endDate = form.endDate.data
        user = current_user.id

        country = form.country.data
        country = string.capwords(country)
        if Country.query.filter_by(name=form.country.data).first() is not None:
            c = Country.query.filter_by(name=form.country.data).first()
        else:
            c = Country(name=form.country.data)
            db.session.add(c)
            db.session.commit()
        city = form.city.data
        city = string.capwords(city)
        if City.query.filter_by(name=form.country.data).first() is not None:
            city1 = City.query.filter_by(name=form.country.data).first()
        else:
            city1 = City(name=city, countryID=c.id)
            db.session.add(city1)
            db.session.commit()

        p = Post(type=type, blog=blog, StartDate=startDate, EndDate=endDate, cityID=city1.id, userID=user)
        db.session.add(p)
        db.session.commit()
        flash('Blog Posted')
        return redirect('/wishList')
    return render_template('wishNew.html', title='New Wish Post', form=form)




@app.route('/explore', methods=['GET', 'POST'])
def explore():
    return render_template('explore.html', title='Explore')


@app.route('/photo-album', methods=['GET', 'POST'])
@login_required
def photoAlbum():
    return render_template('photo-album.html', title='Photo Album')


@app.route('/spot-highlight', methods=['GET', 'POST'])
@login_required
def spotHighlight():
    return render_template('spot-highlight.html', title='Trip Highlight')

