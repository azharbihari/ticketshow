from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import or_
from flask import request
from models import User, db, Theater, Show, ShowStatus, Role
from flask_restful import Resource, marshal, reqparse, marshal_with, fields
from flask_security import auth_required, current_user, SQLAlchemyUserDatastore
from api.marshals import theater_marshal, show_marshal
from cache import cache


class HomeResource(Resource):
    @cache.cached(timeout=300, query_string=True)
    @marshal_with(show_marshal)
    def get(self, show_id=None):
        current_datetime = datetime.now(timezone('Asia/Kolkata'))
        try:
            shows = Show.get_latest_shows()
            return shows, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class SingleShowResource(Resource):
    @marshal_with(show_marshal)
    def get(self, show_id):
        try:
            show = db.get_or_404(Show, show_id)
            if not show:
                return {'message': 'Show not found'}, 404
            return show, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class SearchResource(Resource):
    def get(self):
        try:
            search_term = request.args.get('searchTerm', '')
            theaters = Theater.query.filter(or_(Theater.name.ilike(
                f'%{search_term}%'), Theater.city.ilike(f'%{search_term}%'))).all()

            running_or_upcoming_shows_theaters = [theater for theater in theaters if any(
                show.status in [ShowStatus.RUNNING, ShowStatus.UPCOMING] for show in theater.shows)]

            shows = Show.query.filter(Show.name.ilike(f'%{search_term}%'), Show.status.in_(
                [ShowStatus.RUNNING, ShowStatus.UPCOMING])).all()

            data = {
                'shows': marshal(shows, show_marshal),
                'theaters': marshal(running_or_upcoming_shows_theaters, theater_marshal)
            }

            return data, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class UserCityShowResource(Resource):
    @auth_required()
    @marshal_with(show_marshal)
    def get(self):
        try:
            user = current_user
            if not user:
                return {'message': 'User not found'}, 404
            shows = Show.get_running_or_upcoming_shows_in_city(
                user.city)
            return shows, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class TheaterShowResource(Resource):
    def get(self, theater_id):
        try:
            theater = db.get_or_404(Theater, theater_id)
            if not theater:
                return {'message': 'Theater not found'}, 404
            shows = theater.get_running_or_upcoming_shows()

            data = {
                'shows': marshal(shows, show_marshal),
                'theater': marshal(theater, theater_marshal)
            }

            return data, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500
