from datetime import datetime
import time
import imghdr
import os
from models import User, db, Show, Booking, ShowStatus, BookingStatus, Role, Review, Theater
from flask_restful import Resource, marshal, marshal_with, reqparse
from werkzeug.utils import secure_filename
from flask_security import auth_required, current_user, SQLAlchemyUserDatastore, roles_required
from api.marshals import user_marshal, review_marshal, booking_marshal
from api.parsers import user_parser, booking_parser, avatar_parser, review_parser
from cache import cache
from flask import request


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class ProfileResource(Resource):
    @auth_required()
    @marshal_with(user_marshal)
    def get(self):
        try:
            user = current_user
            user.theaters = Theater.query.all()
            if not user:
                return {'message': 'User not found'}, 404
            return user, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    def put(self):
        try:
            args = user_parser.parse_args()
            user = current_user
            if not all(args.values()):
                return {'message': 'All fields are required'}, 400

            if not user:
                return {'message': 'User not found'}, 404

            user.first_name = args.get('first_name', user.first_name)
            user.last_name = args.get('last_name', user.last_name)
            user.city = args.get('city', user.city)
            user.date_of_birth = args.get('date_of_birth', user.date_of_birth)
            db.session.commit()

            return {'message': 'Profile updated successfully'}, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class AvatarResource(Resource):
    @auth_required()
    def put(self):
        try:
            args = avatar_parser.parse_args()

            user = current_user

            if not user:
                return {'message': 'User not found'}, 404

            avatar = args['avatar']

            if not avatar:
                return {'message': 'Avatar file is required'}, 400

            if avatar and imghdr.what(avatar.stream):
                if user.avatar and user.avatar != "default_avatar.png":
                    old_avatar_path = os.path.join(
                        'media/avatars', user.avatar)
                    if os.path.exists(old_avatar_path):
                        os.remove(old_avatar_path)

                filename = secure_filename(
                    f"{user.id}_{time.time()}_{avatar.filename}")
                avatar.save(os.path.join('media/avatars', filename))
                user.avatar = filename
                db.session.commit()
                cache.clear()

                return {'message': 'Avatar updated successfully'}, 200
            else:
                return {'message': 'Invalid avatar file'}, 400
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class MyBookingResource(Resource):
    @auth_required()
    @marshal_with(booking_marshal)
    def get(self):
        try:
            user = current_user
            if not user:
                return {'message': 'User not found'}, 404

            return user.get_all_bookings(), 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    def post(self, show_id):
        try:
            args = booking_parser.parse_args()
            number_of_tickets = args['number_of_tickets']
            if number_of_tickets <= 0:
                return {'message': 'Invalid number of tickets'}, 400

            show = db.get_or_404(Show, show_id)
            user = current_user

            if show.status == ShowStatus.FINISHED:
                return {'message': 'Cannot book for a finished show'}, 400

            if show.available_tickets < number_of_tickets:
                return {'message': 'Not enough tickets available'}, 400

            booking = Booking(
                number_of_tickets=number_of_tickets, user=user, show=show)
            db.session.add(booking)

            if show.status == ShowStatus.UPCOMING:
                show.available_tickets -= number_of_tickets

            db.session.commit()

            return {'message': 'Booking created successfully'}, 201
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    def delete(self, booking_id):
        try:
            booking = db.get_or_404(Booking, booking_id)
            user = current_user
            show = booking.show

            if booking.user != user:
                return {'message': 'Booking not found'}, 404

            if show.status != ShowStatus.UPCOMING:
                return {'message': 'Cannot cancel booking for a past show'}, 400

            show.available_tickets += booking.number_of_tickets

            booking.status = BookingStatus.CANCELLED
            booking.cancelled_at = datetime.utcnow()
            db.session.commit()

            return {'message': 'Booking cancelled successfully'}, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class MyReviewResource(Resource):
    @auth_required()
    def post(self, booking_id):
        try:
            args = review_parser.parse_args()
            user = db.get_or_404(User, current_user.id)
            booking = db.get_or_404(Booking, booking_id)

            if not all(args.values()):
                return {'message': 'All fields are required'}, 400

            if not booking:
                return {'message': 'Booking not found'}, 404

            if booking.user != user:
                return {'message': 'Booking not found'}, 403

            if booking.review:
                return {'message': 'Review already submitted for this booking'}, 400

            show = booking.show
            if not show:
                return {'message': 'Show not found'}, 404

            review = Review(booking=booking, user=user, show=show, **args)
            db.session.add(review)
            db.session.commit()

            return {'message': 'Review created successfully'}, 201
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    @marshal_with(booking_marshal)
    def get(self):
        try:
            user = current_user
            if not user:
                return {'message': 'User not found'}, 404
            bookings = user.get_confirmed_finished_bookings()
            return bookings, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    def delete(self, booking_id):
        try:
            user = current_user
            booking = db.get_or_404(Booking, booking_id)
            review = booking.review
            if not review:
                return {'message': 'Review not found for this booking'}, 404

            if review.user != user:
                return {'message': 'Review not found'}, 403

            db.session.delete(review)
            db.session.commit()
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500
