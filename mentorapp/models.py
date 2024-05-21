import uuid
from datetime import datetime
from mentorapp import db, app, loginmanager
from flask_login import UserMixin


@loginmanager.user_loader
def load_user(id):
    return User.query.get(id)

class BaseModel:
    ''' Basemodel class'''
    id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        ''' init function'''
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __repr__(self):
        ''' string representation of the class'''
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

app.app_context().push()
class Mentor(BaseModel, db.Model):
    """ Mentor class"""
    __tablename__ = 'mentors'
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    grand_father_name = db.Column(db.String(100), nullable=False)
    Bio = db.Column(db.Text)
    experience = db.Column(db.String(30))
    photo = db.Column(db.String(100), nullable=False, default='default.jpg')
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(100), nullable=False)



class User(BaseModel, db.Model, UserMixin):
    ''' users table'''
    __tablename__ = 'users'
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    grand_father_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Enum('Parent', 'student'))
    students = db.relationship("Student", back_populates="user", cascade="all, delete, delete-orphan")

class Student(BaseModel, db.Model):
    '''Student class'''
    __tablename__ = 'students'
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    grand_father_name = db.Column(db.String(100), nullable=False)
    grade_level = db.Column(db.Integer)
    phone_number = db.Column(db.String(14), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship("User", back_populates="students")

class MentorRequest(BaseModel, db.Model):
    __tablename__ = 'mentor_requests'
    student_id = db.Column(
        db.String(60), db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    mentor_id = db.Column(
        db.String(60), db.ForeignKey('mentors.id', ondelete='CASCADE'), nullable=False)
    request_status = db.Column(db.Enum('Pending', 'Accepted', 'Rejected'))
    description = db.Column(db.Text)
    student = db.relationship(
        "Student", backref="mentor_requests", cascade="all, delete, delete-orphan", single_parent=True)
    mentor = db.relationship(
        "Mentor", backref="mentor_requests", cascade="all,delete, delete-orphan", single_parent=True)
