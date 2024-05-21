from wtforms import Form, TextAreaField, IntegerField, BooleanField, StringField, PasswordField, validators, SelectField, SubmitField
from mentorapp.models import User, Mentor, MentorRequest, Student
import pycountry
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Length, DataRequired, EqualTo


class RegistrationForm(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])
    father_name = StringField('Father name', [validators.Length(min=4, max=25)])
    grand_father_name = StringField('Grand Father name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    phone_number = StringField('phone number', [validators.Length(min=6, max=35)])
    user_type = SelectField('User Type', choices=[('parent', 'Parent'), ('student', 'Student')])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise validators.ValidationError('The email exists. Please use another email!')


class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember me')

class UpdateUserAccount(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])
    father_name = StringField('Father name', [validators.Length(min=4, max=25)])
    grand_father_name = StringField('Grand Father name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    phone_number = StringField('phone number', [validators.Length(min=6, max=35)])
    user_type = SelectField('User Type', choices=[('parent', 'Parent'), ('student', 'Student')])


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise validators.ValidationError('The email exists. Please use another email!')

class StudentRegistration(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])
    father_name = StringField('Father name', [validators.Length(min=4, max=25)])
    grand_father_name = StringField('Grand Father name', [validators.Length(min=4, max=25)])
    grade_level = SelectField('Grade level', choices=[(i, str(i)) for i in range(1, 13)])
    phone_number = StringField('phone number', [validators.Length(min=6, max=35)])

class MentorRegistration(FlaskForm):
    name = StringField('name', validators=[Length(min=4, max=25)])
    father_name = StringField('Father name', validators=[Length(min=4, max=25)])
    grand_father_name = StringField('Grand Father name', validators=[Length(min=4, max=25)])
    phone_number = StringField('Phone number', validators=[Length(min=6, max=35)])
    Bio = TextAreaField('Bio')
    experience = TextAreaField('Experience')
    email = StringField('Email Address', validators=[Length(min=6, max=35)])
    password = PasswordField('New Password', validators=[DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
