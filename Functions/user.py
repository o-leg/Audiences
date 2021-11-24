from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
#from flask_bcrypt import Bcrypt
from models import User, Session, Reservation
from validation_schemas import UserSchema

user = Blueprint('user', __name__)
#bcrypt = Bcrypt()

session = Session()


# Create new user
@user.route('/api/v1/user', methods=['POST'])
def create_user():
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user already exists
    exists = session.query(User.username).filter_by(username=data['username']).first()
    if exists:
        return Response(status=400, response='User with such username already exists.')

    # Create new user
    new_user = User(name=data['name'], surname=data['surname'], username=data['username'], password=data['password'])

    # Add new user to db
    session.add(new_user)
    session.commit()

    return Response(response='New user was successfully created!')




# Get user by id
@user.route('/api/v1/user/<userId>', methods=['GET'])
def get_user(userId):
    # Check if user exists
    db_user = session.query(User).filter_by(id=userId).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')

    # Return user data
    user_data = {'id': db_user.id, 'name': db_user.name, 'surname': db_user.surname, 'username': db_user.username}
    return jsonify({"user": user_data})


# Update user by id
@user.route('/api/v1/user/<userId>', methods=['PUT'])
def update_user(userId):
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user exists
    db_user = session.query(User).filter_by(id=userId).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')

    # Check if username is not taken if user tries to change it
    if 'username' in data.keys():
        exists = session.query(User.id).filter_by(username=data['username']).first()
        if exists:
            return Response(status=400, response='User with such username already exists.')
        db_user.username = data['username']
    # Change user data
    if 'name' in data.keys():
        db_user.name = data['name']
    if "surname" in data.keys():
        db_user.surname = data['surname']
    if 'password' in data.keys():
        hashed_password = bcrypt.generate_password_hash(data['password'])
        db_user.password = hashed_password

    # Save changes
    session.commit()

    # Return new user data
    user_data = {'id': db_user.id, 'name': db_user.name, 'surname': db_user.surname, 'username': db_user.username}
    return jsonify({"user": user_data})


# Delete user by id
@user.route('/api/v1/user/<userId>', methods=['DELETE'])
def delete_user(userId):
    # Check if user exists
    db_user = session.query(User).filter_by(id=userId).first()
    if not db_user:
        return Response(status=404, response='A user with provided ID was not found.')

    # Delete user`s reservations
    session.query(Reservation).filter_by(user_id=userId).delete(synchronize_session="fetch")

    # Delete user
    session.delete(db_user)
    session.commit()
    return Response(response='User was deleted.')