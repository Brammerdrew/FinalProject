from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from models import db, User, Dog, dog_schema, dogs_schema, login_manager
from helpers import token_required
from forms import AddDog
from flask_login import current_user, login_required

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some':'value'}

@api.route('/dogs', methods = ['POST'])
@token_required
def add_dog(current_user_token):
    name= request.json['name']
    gender = request.json['gender']
    age = request.json['age']
    breed = request.json['breed']
    owner_id = current_user_token.id

    dog = Dog(name,gender,age,breed,owner_id=owner_id)

    db.session.add(dog)
    db.session.commit()

    response = dog_schema.dump(dog)
    return jsonify(response)

@api.route('/dogs', methods = ['GET'])
@token_required
def get_dogs(current_user_token):
    owner = current_user_token.token
    dogs = Dog.query.filter_by(owner_id=owner).all()
    response = dogs_schema.dump(dogs)
    return jsonify(response)

@api.route('/dogs/<id>', methods = ['GET'])
@token_required
def get_dog(current_user_token, id):
    dog = Dog.query.get(id)
    response = dog_schema.dump(dog)
    return jsonify(response)

@api.route('/dogs/<id>', methods = ['POST', 'PUT'])
@token_required
def update_dog(current_user_token, id):
    dog = Dog.query.get(id)

    dog.name = request.json['name']
    dog.age = request.json['age']
    dog.gender = request.json['gender']
    dog.breed = request.json['breed']
    dog.owner_id = current_user_token.token

    db.session.commit()
    response = dog_schema.dump(dog)
    return jsonify(response)

@api.route('/dogs/<id>', methods = ['DELETE'])
@token_required
def delete_dog(current_user_token, id):
    id = request.json['id']
    current_user_token= current_user_token.token
    dog = Dog.query.get(id)
    db.session.delete(dog)
    db.session.commit()
    response = dog_schema.dump(dog)
    return jsonify(response)

    