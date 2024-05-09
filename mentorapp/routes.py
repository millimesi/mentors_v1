from flask import render_template, url_for, flash, redirect, get_flashed_messages, request
from mentorapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from mentorapp.forms import RegistrationForm, LoginForm
from mentorapp.models import User, Mentor, MentorRequest, Student
from mentorapp.mentor_dic import mentorslist


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/mentors")
def mentors():
    return render_template('mentors.html', mentorslist=mentorslist, title='mentors')

@app.route("/about")
def about():
    return render_template('about.html', title='about')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('mentors'))
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                name=form.name.data,
                father_name=form.father_name.data,
                grand_father_name=form.grand_father_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                password=hashed_password,
                user_type=form.user_type.data
            )
            db.session.add(user)
            db.session.commit()
            flash(f"Your Account is Created successfully! you can login", 'success')
            return redirect(url_for('login'))
        # else:
        #     return ("<h1>Validation Failed<h1>")
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mentors'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f"Login successfully!", 'success')
                return redirect(next_page) if next_page else redirect(url_for('mentors'))
            else: 
                flash(f"Login unsuccessfully! Please check Password and Email", 'failed')
        else:
            return ("<h1>Validation Failed<h1>")
    return render_template('login.html', title='register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='account')

