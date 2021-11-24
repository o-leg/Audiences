from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class UserSchema(Schema):
    name = fields.String(validate=Length(min=3))
    surname = fields.String(validate=Length(min=3))
    username = fields.String(validate=Length(min=3))
    password = fields.String(validate=Length(min=6))


class AudienceSchema(Schema):
    number = fields.Integer(strict=True)
    amount_of_places = fields.Integer(strict=True)
    status = fields.Integer(strict=True, validate=Range(min=0, max=1))


class ReservationSchema(Schema):
    user_id = fields.Integer(strict=True)
    audience_id = fields.Integer(strict=True)
    title = fields.String()
    from_date = fields.DateTime()
    to_date = fields.DateTime()
