from flask import render_template, url_for, flash, redirect, get_flashed_messages, request
from mentorapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from mentorapp.forms import RegistrationForm, LoginForm, UpdateUserAccount, StudentRegistration
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

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    updateAccount_form= UpdateUserAccount(request.form)
    registerStudent_form= StudentRegistration(request.form)
    if request.method == 'POST':
        if updateAccount_form.validate():
            current_user.name = updateAccount_form.name.data
            current_user.father_name = updateAccount_form.father_name.data
            current_user.grand_father_name = updateAccount_form.grand_father_name.data
            current_user.email = updateAccount_form.email.data
            current_user.phone_number = updateAccount_form.phone_number.data
            current_user.user_type = updateAccount_form.user_type.data

            # Create student table in database
            student = Student(
                name=registerStudent_form.name.data,
                father_name=registerStudent_form.father_name.data,
                grand_father_name=registerStudent_form.grand_father_name.data,
                grade_level=registerStudent_form.grade_level.data,
                phone_number=registerStudent_form.phone_number.data,
                email=registerStudent_form.email.data
            )
            db.session.add(student)
            db.session.commit()
            flash(f"Account Updated successfully!", 'success')
            return redirect(url_for('account'))
    elif request.method == 'GET':
        updateAccount_form.name.data = current_user.name
        updateAccount_form.father_name.data = current_user.father_name
        updateAccount_form.grand_father_name.data = current_user.grand_father_name
        updateAccount_form.email.data = current_user.email
        updateAccount_form.phone_number.data = current_user.phone_number
        updateAccount_form.user_type.data = current_user.user_type
        
        # check if the user has students if there is display it
        if current_user.user_type == 'parent':
            student = Student.query.filter_by(user_id=current_user.id).first()
            if student:
                registerStudent_form.name.data = student.name
                registerStudent_form.father_name.data = student.father_name.father_name
                grand_father_name=registerStudent_form.grand_father_name.data = student.grand_father_name
                registerStudent_form.grade_level.data = student.grade_level
                registerStudent_form.phone_number.data = student.phone_number
                registerStudent_form.email.data = student.email
            else:
                flash('Add Students') 
    return render_template('account.html', title='account', update_form=updateAccount_form, Student_form=registerStudent_form)

