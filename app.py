from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required, UserMixin

# Instantiate the Flask application with configurations
secureApp = Flask(__name__)
secureApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secureApp.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-admin-flask-security-db'
secureApp.config['SECRET_KEY'] = 'secretkey'
secureApp.config['SECURITY_PASSWORD_SALT'] = 'none'

# Instantiate the database
db = SQLAlchemy(secureApp)

# Create a table of users and user roles
roles_users_table = db.Table('roles_users',
                            db.Column('people_id', db.Integer(), db.ForeignKey('people.id')),
                            db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

# Define models for the users and user roles
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class People(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users_table)

# Create a datastore and instantiate Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, People, Role)
security = Security(secureApp, user_datastore)

# Create the tables for the users and roles and add a user to the user table
# This decorator registers a function to be run before the first request to the app
#  i.e. calling localhost:5000 from the browser
@secureApp.before_first_request
def create_user():
    # db.drop_all()
    db.create_all()
    user_datastore.create_user(email='admin', password='admin')
    db.session.commit()

# Define the index route
@secureApp.route('/')
@login_required
def index():
    return '<h1>Hey</h1>'
