from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a81ec48251ca802dd70d96da14b419e6'
USER = 'mentors_dev'
PWD = 'Million1234!'
HOST = 'localhost'
DB = 'light_it_mentors_db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}?'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)
loginmanager.login_view = 'login'

from mentorapp import routes