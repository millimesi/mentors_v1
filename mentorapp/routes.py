from flask import render_template, url_for, flash, redirect, get_flashed_messages, request
from mentorapp import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from mentorapp.forms import MentorRegistration, RegistrationForm, LoginForm, UpdateUserAccount, StudentRegistration
from mentorapp.models import User, Mentor, MentorRequest, Student
from mentorapp.mentor_dic import mentorslist
import secrets
import os


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/mentors")
def mentors():
    # mentorslist = Mentor.query.all()
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
    update_form= UpdateUserAccount(request.form)
    Student_form= StudentRegistration(request.form)
    if request.method == 'POST':
        if update_form.validate():
            current_user.name = update_form.name.data
            current_user.father_name = update_form.father_name.data
            current_user.grand_father_name = update_form.grand_father_name.data
            current_user.email = update_form.email.data
            current_user.phone_number = update_form.phone_number.data
            current_user.user_type = update_form.user_type.data
            db.session.commit()
            flash(f"Account Updated successfully!", 'success')
            return redirect(url_for('account'))
    elif request.method == 'GET':
        update_form.name.data = current_user.name
        update_form.father_name.data = current_user.father_name
        update_form.grand_father_name.data = current_user.grand_father_name
        update_form.email.data = current_user.email
        update_form.phone_number.data = current_user.phone_number
        update_form.user_type.data = current_user.user_type
        
        # check if the user has students if there is display it
        student = Student.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', title='account', update_form=update_form, Student_form=Student_form, student=student)


@app.route("/register-student", methods=['GET', 'POST'])
@login_required
def register_Student():
    Student_form= StudentRegistration(request.form)
    if request.method == 'POST':
        if Student_form.validate():
            student = Student(
                name=Student_form.name.data,
                father_name=Student_form.father_name.data,
                grand_father_name=Student_form.grand_father_name.data,
                grade_level=Student_form.grade_level.data,
                phone_number=Student_form.phone_number.data,
                user_id= current_user.id
            )
            db.session.add(student)
            db.session.commit()
            flash(f"Student Registered successfully!", 'success')
            return redirect(url_for('account'))
    return render_template('rstudent.html', title='register-student', Student_form=Student_form)


@app.route("/edit-student/<string:student_id>", methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    Student_form= StudentRegistration(request.form)
    student = Student.query.filter_by(id=student_id).first()
    if request.method == 'GET':
        Student_form.name.data = student.name
        Student_form.father_name.data = student.father_name
        Student_form.grand_father_name.data = student.grand_father_name
        Student_form.grade_level.data = student.grade_level
        Student_form.phone_number.data = student.phone_number
    if request.method == 'POST':
        if Student_form.validate():
            student.name = Student_form.name.data
            student.father_name = student.father_name
            student.grand_father_name = Student_form.grand_father_name.data
            student.grade_level = Student_form.grade_level.data
            student.phone_number = Student_form.phone_number.data
            db.session.commit()
            return redirect(url_for('account'))
    return render_template('rstudent.html', title='edit-student', Student_form=Student_form)


@app.route("/delete-student/<string:student_id>", methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        flash("Student is deleted successfully!", 'success')
    else:
        flash("Student not found!", 'error')
    return redirect(url_for('account'))

def save_pictures(form_photo):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_photo.filename)
    photo_fname = random_hex + f_ext
    photo_path = os.path.join(app.root_path, 'static/images/profile_pics', photo_fname)
    form_photo.save(photo_path)
    return photo_fname

@app.route("/register-mentor", methods=['GET', 'POST'])
def register_mentor():
    mentor_form= MentorRegistration()
    if mentor_form.validate_on_submit():
        mentor = Mentor(
            name=mentor_form.name.data,
            father_name=mentor_form.father_name.data,
            grand_father_name=mentor_form.grand_father_name.data,
            phone_number=mentor_form.phone_number.data,
            Bio = mentor_form.Bio.data,
            experience = mentor_form.experience.data,
            photo = save_pictures(mentor_form.photo.data),
            email = mentor_form.email.data,
            password = bcrypt.generate_password_hash(mentor_form.password.data).decode('utf-8')
        )
        db.session.add(mentor)
        db.session.commit()
        flash(f"Registered as a Mentor successfully!", 'success')
        return redirect(url_for('mentors'))
    else:
        print(mentor_form.errors)
    return render_template('r_mentor.html', title='register-mentor', mentor_form=mentor_form)