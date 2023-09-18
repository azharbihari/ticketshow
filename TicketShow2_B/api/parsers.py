from flask_restful.reqparse import RequestParser
from datetime import datetime
import werkzeug

user_parser = RequestParser()
user_parser.add_argument('first_name', type=str, required=True)
user_parser.add_argument('last_name', type=str, required=True)
user_parser.add_argument('city', type=str, required=True)
user_parser.add_argument(
    'date_of_birth', type=datetime.fromisoformat, required=False)


register_parser = RequestParser()
register_parser.add_argument('email', type=str, required=True)
register_parser.add_argument('password', type=str, required=True)
register_parser.add_argument('first_name', type=str, required=True)
register_parser.add_argument('last_name', type=str, required=True)

login_parser = RequestParser()
login_parser.add_argument('email', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)


booking_parser = RequestParser()
booking_parser.add_argument('number_of_tickets', type=int, required=True)

avatar_parser = RequestParser()
avatar_parser.add_argument(
    'avatar', type=werkzeug.datastructures.FileStorage, location='files')


review_parser = RequestParser()
review_parser.add_argument('rating', type=int, required=True)
review_parser.add_argument('comment', type=str, required=True)


theater_parser = RequestParser()
theater_parser.add_argument('name', type=str, required=True)
theater_parser.add_argument('city', type=str, required=True)
theater_parser.add_argument('capacity', type=int, required=True)


show_parser = RequestParser()
show_parser.add_argument('name', type=str, required=True)
show_parser.add_argument('genre', type=str, required=True)
show_parser.add_argument('description', type=str, required=True)
show_parser.add_argument('language', type=str, required=True)
show_parser.add_argument(
    'showtime', type=datetime.fromisoformat, required=True)
show_parser.add_argument('ticket_price', type=float, required=True)
show_parser.add_argument('runtime', type=int, required=True)


poster_parser = RequestParser()
poster_parser.add_argument(
    'poster', type=werkzeug.datastructures.FileStorage, location='files')
