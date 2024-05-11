from wtforms import Form, IntegerField, BooleanField, StringField, PasswordField, validators, SelectField
from mentorapp.models import User, Mentor, MentorRequest, Student
import pycountry
from flask_login import current_user



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
    grade_level = SelectField('User Type', choices=[(1, '1'), (2, '2'), (1, '3'), (4, '4'),
                        (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'),
                        (10, '10'),(11, '11'), (12, '12')])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    phone_number = StringField('phone number', [validators.Length(min=6, max=35)])

