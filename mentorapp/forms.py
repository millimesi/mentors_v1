from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField
from mentorapp.models import User, Mentor, MentorRequest, Student
import pycountry



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
