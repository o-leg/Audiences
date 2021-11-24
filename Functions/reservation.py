from flask import Response, request, jsonify, Blueprint
from marshmallow import ValidationError
from datetime import datetime
from models import Reservation, User, Audience, Session
from validation_schemas import ReservationSchema

reservation = Blueprint('reservation', __name__)

session = Session()


# Create new reservation
@reservation.route('/api/v1/reservation', methods=['POST'])
def create_reservation():
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        ReservationSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user already exists
    exists = session.query(User.id).filter_by(id=data['user_id']).first()
    if not exists:
        return Response(status=404, response='User with such id was not found.')

    # Check if audience already exists
    exists = session.query(Audience.id).filter_by(id=data['audience_id']).first()
    if not exists:
        return Response(status=404, response='Audience with such id was not found.')

    d1 = datetime.strptime(data['from_date'], '%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(data['to_date'], '%Y-%m-%d %H:%M:%S')

    # Compare if end date is bigger than start date
    if d1 > d2:
        return Response(status=400, response="Invalid dates input. d1 > d2")

    # Check if user wants to reserve audience for allowed period of time
    diff = d2 - d1
    if (diff.total_seconds() / 3600) < 1 or diff.days > 5:
        return Response(status=400, response="Audience cannot be reserved for that period of time. d2 - d1 > 5")

    # Check if audience is available for given date

    all_reserved = session.query(Reservation).all()

    dfrom = datetime.strptime(data['from_date'], '%Y-%m-%d %H:%M:%S')
    dto = datetime.strptime(data['to_date'], '%Y-%m-%d %H:%M:%S')

    for k in all_reserved:
        if k.from_date <= dfrom <= k.to_date:
            return {"message": "1. Class is already reserved for this time."}, 400
        if k.from_date <= dto <= k.to_date:
            return {"message": "2. Class is already reserved for this time."}, 400
        if dfrom <= k.from_date and dto >= k.to_date:
            return {"message": "3. Class is already reserved for this time."}, 400

    # Create new reservation
    new_reservation = Reservation(
        user_id=data['user_id'],
        audience_id=data['audience_id'],
        title=data['title'],
        from_date=data['from_date'],
        to_date=data['to_date']
    )

    # Add new reservation to db
    session.add(new_reservation)
    session.commit()

    return Response(response='New reservation was successfully created!')


# Get all reservations
@reservation.route('/api/v1/reservation', methods=['GET'])
def get_reservations():
    # Get all reservations from db
    reservations = session.query(Reservation)

    # Return all reservations
    output = []
    for r in reservations:
        output.append({'id': r.id,
                       'user_id': r.user_id,
                       'audience_id': r.audience_id,
                       'title': r.title,
                       'from_date': r.from_date,
                       'to_date': r.to_date})
    return jsonify({"reservations": output})


# Get reservation by id
@reservation.route('/api/v1/reservation/<reservationId>', methods=['GET'])
def get_reservation(reservationId):
    # Check if reservation exists
    db_reservation = session.query(Reservation).filter_by(id=reservationId).first()
    if not db_reservation:
        return Response(status=404, response='A reservation with provided ID was not found.')

    # Return reservation data
    reservation_data = {
        'id': db_reservation.id,
        'user_id': db_reservation.user_id,
        'audience_id': db_reservation.audience_id,
        'title': db_reservation.title,
        'from_date': db_reservation.from_date,
        'to_date': db_reservation.to_date
    }
    return jsonify({"reservation": reservation_data})


# Update reservation by id
@reservation.route('/api/v1/reservation/<reservationId>', methods=['PUT'])
def update_reservation(reservationId):
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        ReservationSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if reservation exists
    db_reservation = session.query(Reservation).filter_by(id=reservationId).first()
    if not db_reservation:
        return Response(status=404, response='A reservation with provided ID was not found.')

    if 'from_date' in data.keys():
        d1 = datetime.strptime(data['from_date'], '%Y-%m-%d %H:%M:%S')
    else:
        d1 = db_reservation.from_date
    if 'to_date' in data.keys():
        d2 = datetime.strptime(data['to_date'], '%Y-%m-%d %H:%M:%S')
    else:
        d2 = db_reservation.to_date

    # Check if audience is available for given date if user wants to change dates
    if 'from_date' in data.keys() or 'to_date' in data.keys() or 'audience_id' in data.keys():
        # Compare if end date is bigger than start date
        if d1 > d2:
            return Response(status=400, response="Invalid dates input.")

        # # Check if user wants to reserve audience for allowed period of time
        # diff = d2 - d1
        # if (diff.total_seconds() / 3600) < 1 or diff.days > 5:
        #     return Response(status=400, response="Audience cannot be reserved for that period of time.")

        if 'audience_id' in data.keys():
            audience = session.query(Audience).filter_by(id=data['audience_id']).first()
        else:
            audience = session.query(Audience).filter_by(id=db_reservation.audience_id).first()
        if not audience.status:
            return Response(status=400, response="Audience is not available now.")
        reservations = session.query(Reservation).filter_by(audience_id=audience.id)
        flag = False

        if datetime.strptime(data['from_date'], '%Y-%m-%d %H:%M:%S') > datetime.strptime(data['to_date'],
                                                                                         '%Y-%m-%d %H:%M:%S'):
            return {"message": "Invalid data input. "}

        # for r in reservations:
        #     if db_reservation.id != r.id:
        #         if (r.from_date <= d1 <= r.to_date) or (
        #                 r.from_date <= d2 <= r.to_date) or (
        #                 d1 <= r.from_date and d2 >= r.to_date):
        #             flag = True
        #             break
        # if flag:
        #     return Response(status=400, response='Audience is already reserved for given time.')

    # Change reservation data

    for key, value in data.items():
        setattr(db_reservation, key, value)

    # if 'audience_id' in data.keys():
    #     db_reservation.audience_id = data['audience_id']
    # if 'title' in data.keys():
    #     db_reservation.title = data['title']
    # if 'from_date' in data.keys():
    #     db_reservation.from_date = data['from_date']
    # if 'to_date' in data.keys():
    #     db_reservation.from_date = data['to_date']

    # Save changes
    session.commit()

    # Return new reservation data
    reservation_data = {
        'id': db_reservation.id,
        'user_id': db_reservation.user_id,
        'audience_id': db_reservation.audience_id,
        'title': db_reservation.title,
        'from_date': db_reservation.from_date,
        'to_date': db_reservation.to_date
    }
    return jsonify({"reservation": reservation_data})


# Delete reservation by id
@reservation.route('/api/v1/reservation/<reservationId>', methods=['DELETE'])
def delete_reservation(reservationId):
    # Check if reservation exists
    db_reservation = session.query(Reservation).filter_by(id=reservationId).first()
    if not db_reservation:
        return Response(status=404, response='A reservation with provided ID was not found.')

    # Delete audience
    session.delete(db_reservation)
    session.commit()
    return Response(response='Reservation was deleted.')


# Get all reservations for user with provided id
@reservation.route('/api/v1/reservation/user_id/<userId>', methods=['GET'])
def get_reservations_by_userId(userId):
    # Get all user's reservations from db
    reservations = session.query(Reservation).filter_by(user_id=userId)

    # Return all reservations
    output = []
    for r in reservations:
        output.append({'id': r.id,
                       'user_id': r.user_id,
                       'audience_id': r.audience_id,
                       'title': r.title,
                       'from_date': r.from_date,
                       'to_date': r.to_date})
    return jsonify({"reservations": output})


# Get all reservations for user with provided username
@reservation.route('/api/v1/reservation/username/<username>', methods=['GET'])
def get_reservations_by_username(username):
    # Check if user exists
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return Response(status=404, response='User with such username was not found.')

    # Get all user's reservations from db
    reservations = session.query(Reservation).filter_by(user_id=user.id)

    # Return all reservations
    output = []
    for r in reservations:
        output.append({'id': r.id,
                       'user_id': r.user_id,
                       'audience_id': r.audience_id,
                       'title': r.title,
                       'from_date': r.from_date,
                       'to_date': r.to_date})
    return jsonify({"reservations": output})
