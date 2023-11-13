from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import uuid
from flask_marshmallow import Marshmallow



db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dogs = db.relationship('Dog', backref='owner', lazy=True)
    token = db.Column(db.String, default='', unique=True)

    def __init__(self, first_name, last_name, email, password, token=''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_urlsafe(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has been created and added to database!'

class Dog(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(150), nullable=False) # 'M' or 'F
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(150), nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, gender, age, breed, owner_id):
        self.id = self.set_id()
        self.name = name
        self.gender = gender
        self.age = age
        self.breed = breed
        self.owner_id = owner_id

    def set_id(self):
        return (secrets.token_urlsafe())
    
    def __repr__(self):
        return f'The following dog has been added: {self.name}'
    
class DogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'gender', 'age', 'breed', 'owner_id')

dog_schema = DogSchema()
dogs_schema = DogSchema(many=True)