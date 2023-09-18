from flask_security import SQLAlchemyUserDatastore
from flask_restful import marshal, fields


class AvatarFormat(fields.Raw):
    def format(self, value):
        return f"http://127.0.0.1:5000/media/avatars/{value}" if value else None


class PosterFormat(fields.Raw):
    def format(self, value):
        return f"http://127.0.0.1:5000/media/posters/{value}" if value else None


role_marshal = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}


theater_marshal = {
    'id': fields.Integer,
    'name': fields.String,
    'city': fields.String,
    'capacity': fields.Integer,
    'slug': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
}

user_marshal = {
    'id': fields.Integer,
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'city': fields.String,
    'date_of_birth': fields.DateTime(dt_format='iso8601'),
    'avatar': AvatarFormat(attribute='avatar'),
    'roles': fields.List(fields.Nested(role_marshal)),
    'theaters': fields.List(fields.Nested(theater_marshal))
}

show_marshal = {
    'id': fields.Integer,
    'name': fields.String,
    'slug': fields.String,
    'genre': fields.String,
    'description': fields.String,
    'language': fields.String,
    'runtime': fields.Integer,
    'showtime': fields.DateTime(dt_format='iso8601'),
    'status': fields.String(attribute=lambda show: show.status.value if show else None),
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
    'available_tickets': fields.Integer,
    'ticket_price': fields.Float,
    'theater': fields.Nested(theater_marshal),
    'poster': PosterFormat(attribute='poster'),
    'is_housefull': fields.Boolean(attribute=lambda show: show.available_tickets == 0)
}

review_marshal = {
    'id': fields.Integer,
    'user': fields.Nested(user_marshal),
    'show': fields.Nested(show_marshal),
    'rating': fields.Integer,
    'comment': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601')
}

booking_marshal = {
    'id': fields.Integer,
    'user': fields.Nested(user_marshal),
    'show': fields.Nested(show_marshal),
    'number_of_tickets': fields.Integer,
    'amount': fields.Float,
    'status': fields.String(attribute=lambda booking: booking.status.value if booking else None),
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
    'review': fields.Raw(attribute=lambda booking: marshal(booking.review, review_marshal) if booking.review else None)
}
