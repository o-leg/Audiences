from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError

from passlib.hash import bcrypt

#from flask_bcrypt import Bcrypt

from models import User, Session
from validation_schemas import UserSchema

auth = Blueprint('auth', __name__)

#bcrypt = Bcrypt()

session = Session()


# Register new user
@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user already exists
    exists = session.query(User.id).filter_by(username=data['username']).first()
    if exists:
        return Response(status=400, response='User with such username already exists.')

    # Hash user's password
    hashed_password = bcrypt.generate_password_hash(data['password'])
    # Create new user
    new_user = User(name=data['name'], surname=data['surname'], username=data['username'], password=hashed_password)

    # Add new user to db
    session.add(new_user)
    session.commit()

    return Response(response='New user was successfully created!')