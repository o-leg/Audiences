from flask import Response, request, jsonify, Blueprint
from marshmallow import ValidationError
from models import Audience, Session
from validation_schemas import AudienceSchema

audience = Blueprint('audience', __name__)

session = Session()


# Create new audience
@audience.route('/api/v1/audience', methods=['POST'])
def create_audience():
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        AudienceSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if audience already exists
    exists = session.query(Audience.id).filter_by(number=data['number']).first()
    if exists:
        return Response(status=400, response='Audience with such number already exists.')

    # Create new audience
    new_audience = Audience(number=data['number'], amount_of_places=data['amount_of_places'], status=data['status'])

    # Add new audience to db
    session.add(new_audience)
    session.commit()

    return Response(response='New audience was successfully created!')


# Get all audiences
@audience.route('/api/v1/audience', methods=['GET'])
def get_audiences():
    # Get all audiences from db
    audiences = session.query(Audience)

    # Return all audiences
    output = []
    for a in audiences:
        output.append({'id': a.id,
                       'number': a.number,
                       'amount_of_places': a.amount_of_places,
                       'status': a.status})
    return jsonify({"audiences": output})


# Get audience by id
@audience.route('/api/v1/audience/<audienceId>', methods=['GET'])
def get_audience(audienceId):
    # Check if audience exists
    db_audience = session.query(Audience).filter_by(id=audienceId).first()
    if not db_audience:
        return Response(status=404, response='An audience with provided ID was not found.')

    # Return audience data
    audience_data = {
        'id': db_audience.id,
        'number': db_audience.number,
        'amount_of_places': db_audience.amount_of_places,
        'status': db_audience.status
    }
    return jsonify({"audience": audience_data})


# Update audience by id
@audience.route('/api/v1/audience/<audienceId>', methods=['PUT'])
def update_audience(audienceId):
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        AudienceSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if audience exists
    db_audience = session.query(Audience).filter_by(id=audienceId).first()
    if not db_audience:
        return Response(status=404, response='An audience with provided ID was not found.')

    # Check if audience with such number already exists
    if 'number' in data.keys():
        exists = session.query(Audience.id).filter_by(number=data['number']).first()
        if exists:
            return Response(status=400, response='Audience with such number already exists.')
        db_audience.number = data['number']
    # Change audience data
    if 'amount_of_places' in data.keys():
        db_audience.amount_of_places = data['amount_of_places']
    if 'status' in data.keys():
        db_audience.status = data['status']

    # Save changes
    session.commit()

    # Return new audience data
    audience_data = {
        'id': db_audience.id,
        'number': db_audience.number,
        'amount_of_places': db_audience.amount_of_places,
        'status': db_audience.status
    }
    return jsonify({"audience": audience_data})


# Delete audience by id
@audience.route('/api/v1/audience/<audienceId>', methods=['DELETE'])
def delete_audience(audienceId):
    # Check if audience exists
    db_audience = session.query(Audience).filter_by(id=audienceId).first()
    if not db_audience:
        return Response(status=404, response='An audience with provided ID was not found.')

    # Delete audience
    session.delete(db_audience)
    session.commit()
    return Response(response='Audience was deleted.')