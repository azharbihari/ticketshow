from datetime import datetime, timedelta
from operator import and_
from flask import abort, url_for
import time
import imghdr
import os
from sqlalchemy import or_
import werkzeug
from models import db, Theater, Show
from flask_restful import Resource, reqparse, marshal_with, marshal
from werkzeug.utils import secure_filename
from flask_security import auth_required, roles_required
from api.marshals import show_marshal, theater_marshal
from api.parsers import show_parser, poster_parser
from flask import jsonify


class ShowResource(Resource):
    @auth_required()
    @roles_required('admin')
    def get(self, theater_id):
        try:
            theater = db.get_or_404(Theater, theater_id)
            if not theater:
                return {'message': 'Theater not found'}, 404

            shows = theater.get_all_shows()
            return {'theater': marshal(theater, theater_marshal), 'shows': marshal(shows, show_marshal)}, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    @roles_required('admin')
    def post(self, theater_id):
        try:

            args = show_parser.parse_args()
            theater = db.get_or_404(Theater, theater_id)
            if not theater:
                return {'message': 'Theater not found'}, 404

            if args['showtime'] <= datetime.now():
                return {'message': 'Show time must be in the future'}, 400

            overlapping_shows = Show.query.filter(
                Show.theater == theater,
                or_(
                    and_(
                        Show.showtime >= args['showtime'],
                        Show.showtime < args['showtime'] +
                        timedelta(minutes=args['runtime'])
                    ),
                    and_(
                        Show.end_showtime > args['showtime'],
                        Show.end_showtime <= args['showtime'] +
                        timedelta(minutes=args['runtime'])
                    ),
                    and_(
                        Show.showtime <= args['showtime'],
                        Show.end_showtime >= args['showtime'] +
                        timedelta(minutes=args['runtime'])
                    )
                )
            ).all()

            if overlapping_shows:
                return {'message': 'Show time overlaps with an existing show'}, 409

            show = Show(**args, theater=theater)
            db.session.add(show)
            db.session.commit()
            return {'message': 'Show created successfully'}, 201
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    @roles_required('admin')
    def delete(self, show_id):
        try:
            show = db.get_or_404(Show, show_id)
            if not show:
                return {'message': 'Show not found'}, 404

            db.session.delete(show)
            db.session.commit()
            return {'message': 'Show deleted successfully'}, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    @roles_required('admin')
    def put(self, show_id):
        try:
            args = show_parser.parse_args()
            show = db.get_or_404(Show, show_id)
            if not show:
                return {'message': 'Show not found'}, 404

            if args['showtime'] <= datetime.now():
                return {'message': 'Show time must be in the future'}, 400

            overlapping_shows = Show.query.filter(
                Show.id != show.id,
                or_(
                    and_(
                        Show.showtime >= args['showtime'],
                        Show.showtime < args['showtime'] +
                        timedelta(minutes=args['runtime'])
                    ),
                    and_(
                        Show.end_showtime > args['showtime'],
                        Show.end_showtime <= args['showtime'] +
                        timedelta(minutes=args['runtime'])
                    ),
                    and_(
                        Show.showtime <= args['showtime'],
                        Show.end_showtime >= args['showtime'] +
                        timedelta(minutes=args['runtime'])
                    )
                )
            ).all()

            if overlapping_shows:
                return {'message': 'Show time overlaps with an existing show'}, 409

            show.name = args.get('name', show.name)
            show.genre = args.get('genre', show.genre)
            show.description = args.get('description', show.description)
            show.language = args.get('language', show.language)
            show.showtime = args.get('showtime', show.showtime)
            show.end_showtime = args['showtime'] + \
                timedelta(minutes=args['runtime'])
            show.available_tickets = args.get(
                'available_tickets', show.available_tickets)
            show.ticket_price = args.get('ticket_price', show.ticket_price)
            show.runtime = args.get('runtime', show.runtime)

            db.session.commit()

            return {'message': 'Show updated successfully'}, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class PosterResource(Resource):
    @auth_required()
    @roles_required('admin')
    def put(self, show_id):
        try:
            args = poster_parser.parse_args()

            show = db.get_or_404(Show, show_id)
            if not show:
                return {'message': 'Show not found'}, 404

            poster = args['poster']

            if not poster:
                return {'message': 'Poster file is required'}, 400

            if poster and imghdr.what(poster.stream):
                if show.poster and show.poster != "default_poster.png":
                    old_poster_path = os.path.join(
                        'media/posters', show.poster)
                    if os.path.exists(old_poster_path):
                        os.remove(old_poster_path)

                filename = secure_filename(
                    f"{show.id}_{time.time()}_{poster.filename}")
                poster.save(os.path.join('media/posters', filename))
                show.poster = filename
                db.session.commit()
                return {'message': 'Poster updated successfully'}, 200
            else:
                return {'message': 'Invalid poster file'}, 400

        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500
