import os
from typing import re

from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, \
    SelectMultipleField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, City, Country, Post
from wtforms.fields.html5 import DateField, DateTimeField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
       'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
       user = User.query.filter_by(username=username.data).first()
       if user is not None:
           raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class NewWish(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    blog = TextAreaField('Dream Trip', validators=[DataRequired()])
    startDate = DateTimeField('Start Date (MM-DD-YYYY)', format='%m-%d-%Y')
    endDate = DateTimeField('End Date (MM-DD-YYYY)', format='%m-%d-%Y')
    submit = SubmitField('Add Trip')

'''
    image = MultipleFileField(u'Image File', [validators.regexp(u'^[^/\\]\.jpg$')])
    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
'''
'''
    def upload(request):
        form = NewWish(request.POST)
        if form.image.data:
            image_data = request.FILES[form.image.name].read()
            open(os.path.join('app/images', form.image.data), 'w').write(image_data)
'''


class NewBeen(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    blog = TextAreaField('Blog Post', validators=[DataRequired()])
    startDate = DateTimeField('Start Date (MM-DD-YYYY)', format='%m-%d-%Y')
    endDate = DateTimeField('End Date (MM-DD-YYYY)', format='%m-%d-%Y')
    submit = SubmitField('Add Trip')

    '''
    image = MultipleFileField(u'Image File', [validators.regexp(u'^[^/\\]\.jpg$')])

    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)
'''
    '''
    def upload(request):
        form = NewBeen(request.POST)
        if form.image.data:
            image_data = request.FILES[form.image.name].read()
            open(os.path.join('app/images', form.image.data), 'w').write(image_data)

'''