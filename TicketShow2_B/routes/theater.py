from flask import jsonify, url_for
from sqlalchemy import desc, distinct, func
from models import db, Theater, UserActivity, Show, User, Review, Booking, BookingStatus
from flask_restful import Resource, marshal_with, marshal
from tasks import export_theater_data_to_csv
from celery.result import AsyncResult
from flask_security import auth_required, current_user, roles_required
from api.marshals import theater_marshal, show_marshal, user_marshal
from api.parsers import theater_parser
from cache import cache
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')


class TheaterResource(Resource):
    @staticmethod
    def key_prefix():
        return f'theaters:{current_user.id}'

    @auth_required()
    @roles_required('admin')
    @cache.cached(timeout=300, key_prefix=key_prefix)
    @marshal_with(theater_marshal)
    def get(self):
        try:
            user = current_user
            if not user:
                return {'message': 'User not found'}, 404
            theaters = user.get_all_theaters()
            return theaters, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    @roles_required('admin')
    def post(self):
        try:
            args = theater_parser.parse_args()
            if not all(args.values()):
                return {'message': 'All fields are required'}, 400

            capacity = args['capacity']
            if capacity <= 0:
                return {'message': 'Capacity must be greater than 0'}, 400

            theater = Theater(**args, user=current_user)
            db.session.add(theater)
            db.session.commit()
            cache.delete(self.key_prefix())
            return {'message': 'Theater created successfully!'}, 201
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    @roles_required('admin')
    def delete(self, theater_id):
        try:
            theater = Theater.query.get_or_404(theater_id)
            if not theater:
                return {'message': 'Theater not found'}, 404
            db.session.delete(theater)
            db.session.commit()
            cache.delete(self.key_prefix())
            return {'message': 'Theater deleted successfully!'}, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    @auth_required()
    @roles_required('admin')
    def put(self, theater_id):
        try:
            args = theater_parser.parse_args()
            theater = Theater.query.get_or_404(theater_id)
            if not theater:
                return {'message': 'Theater not found'}, 404

            if not all(args.values()):
                return {'message': 'All fields are required'}, 400

            capacity = args['capacity']
            if capacity <= 0:
                return {'message': 'Capacity must be greater than 0'}, 400

            theater.name = args.get('name', theater.name)
            theater.city = args.get('city', theater.city)
            theater.capacity = args.get('capacity', theater.capacity)
            db.session.commit()
            cache.delete(self.key_prefix())
            return {'message': 'Theater updated successfully!'}, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class ExportResource(Resource):
    @auth_required()
    @roles_required('admin')
    def get(self, theater_id):
        try:
            theater = db.get_or_404(Theater, theater_id)
            if not theater:
                return {'message': 'Theater not found'}, 404

            task = export_theater_data_to_csv.apply_async(
                args=(theater.id,), countdown=5)

            return str(task.id), 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class ExportStatusResource(Resource):
    @auth_required()
    @roles_required('admin')
    def get(self, task_id):
        try:
            task = AsyncResult(task_id)

            if not task:
                return {'message': 'Task not found'}, 404

            response = {
                'status': task.status,
                'csv_url': None
            }

            if task.ready():
                if task.successful():
                    response['csv_url'] = url_for(
                        'download', filename=task.result, _external=True)
                else:
                    response['message'] = 'Task did not complete successfully'
            else:
                response['message'] = 'Task is still running'

            return response, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500


class InsightResource(Resource):
    @auth_required()
    @roles_required('admin')
    def get(self):
        try:
            user = current_user
            if not user:
                return {'message': 'User not found'}, 404

            from sqlalchemy import func

            def get_most_visited_show():
                most_visited_show = Show.query.join(UserActivity).group_by(
                    Show.id).order_by(func.sum(UserActivity.visit_count).desc()).first()
                return most_visited_show

            def get_most_active_user():
                most_active_user = User.query.join(UserActivity).group_by(
                    User.id).order_by(func.sum(UserActivity.visit_count).desc()).first()
                return most_active_user

            def get_top_5_most_visited_shows():
                top_5_most_visited_shows = Show.query.join(UserActivity).group_by(
                    Show.id).order_by(func.sum(UserActivity.visit_count).desc()).limit(5).all()
                return top_5_most_visited_shows

            def get_top_5_highest_rated_shows():
                top_5_highest_rated_shows = Show.query.join(Review).group_by(
                    Show.id).order_by(func.avg(Review.rating).desc()).limit(5).all()
                return top_5_highest_rated_shows

            def get_top_5_shows_with_unique_visitors():
                top_5_shows_with_unique_visitors = Show.query.join(UserActivity).group_by(
                    Show.id).order_by(func.count(distinct(UserActivity.user_id)).desc()).limit(5).all()
                return top_5_shows_with_unique_visitors

            def get_total_number_of():
                bookings = Booking.query.filter(
                    Booking.status == BookingStatus.CONFIRMED).count()
                shows = Show.query.count()
                theaters = Theater.query.count()
                reviews = Review.query.count()
                users = User.query.count()
                return {'bookings': bookings, 'shows': shows, 'theaters': theaters, 'reviews': reviews, 'users': users}

            def get_top_5_highest_spending_users():
                top_5_highest_spending_users = User.query.join(Booking).group_by(
                    User.id).order_by(func.sum(Booking.amount).desc()).limit(5).all()
                return top_5_highest_spending_users

            def get_city_with_most_active_users():
                city_with_most_active_users = (
                    User.query
                    .join(UserActivity)
                    .group_by(User.city)
                    .order_by(func.count(UserActivity.id).desc())
                    .first()
                )
                return city_with_most_active_users

            def get_top_five_shows_by_revenue():
                revenue_per_show = db.session.query(Show, func.sum(Booking.amount).label('revenue')).\
                    join(Booking).\
                    group_by(Show.id).\
                    order_by(desc('revenue')).\
                    limit(5).all()

                show_names = [show.name for show, revenue in revenue_per_show]
                revenue_values = [revenue for show,
                                  revenue in revenue_per_show]

                plt.bar(show_names, revenue_values, color=[
                        '#1f77b4', '#2ca02c', '#9467bd', '#ff7f0e', '#17becf'])
                plt.xlabel('Shows')
                plt.ylabel('Revenue')
                plt.tight_layout()
                plt.savefig('media/charts/top_five_shows_by_revenue.png')
                plt.clf()
                return 'http://127.0.0.1:5000/media/charts/top_five_shows_by_revenue.png'

            def get_user_activity_funnel_analysis():
                visits = UserActivity.query.join(
                    Show).group_by(UserActivity.id).count()
                bookings = Booking.query.count()
                reviews = Review.query.count()

                visit_to_booking_conversion_rate = bookings / visits if visits > 0 else 0
                booking_to_review_conversion_rate = reviews / bookings if bookings > 0 else 0

                stages = ['Visits', 'Bookings', 'Reviews']
                conversion_rates = [
                    1, visit_to_booking_conversion_rate, booking_to_review_conversion_rate]
                plt.figure(figsize=(12, 8))
                plt.bar(stages, conversion_rates, color=[
                        'tab:red', 'tab:green', 'tab:blue'])
                plt.xlabel('Stages')
                plt.ylabel('Conversion Rate')
                plt.savefig('media/charts/user_activity_funnel.png')
                plt.clf()
                return 'http://127.0.0.1:5000/media/charts/user_activity_funnel.png'

            insights = {
                'most_visited_show': marshal(get_most_visited_show(), show_marshal),
                'most_active_user': marshal(get_most_active_user(), user_marshal),
                'top_5_most_visited_shows': marshal(get_top_5_most_visited_shows(), show_marshal),
                'top_5_highest_rated_shows': marshal(get_top_5_highest_rated_shows(), show_marshal),
                'top_5_shows_with_unique_visitors': marshal(get_top_5_shows_with_unique_visitors(), show_marshal),
                'total_number_of': get_total_number_of(),
                'top_5_highest_spending_users': marshal(get_top_5_highest_spending_users(), user_marshal),
                'city_with_most_active_users': marshal(get_city_with_most_active_users(), theater_marshal),
                'user_activity_funnel_analysis': get_user_activity_funnel_analysis(),
                'top_five_shows_by_revenue': get_top_five_shows_by_revenue()
            }
            return insights, 200
        except Exception as e:
            return {'message': 'Internal Server Error', 'error': str(e)}, 500
