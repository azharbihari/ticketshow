from datetime import timedelta
import os
from flask_caching import Cache
from flask import Flask, send_from_directory, request
from flask_cors import CORS
from sqlalchemy import text
from config import Config
from models import db
from flask_security import Security, SQLAlchemyUserDatastore, hash_password, current_user
from make_celery import celery_init_app
from tasks import update_show_status, update_dynamic_price, add_user_activity, mail, send_inactive_user_email, send_monthly_entertainment_report
from models import User, Role
from celery.schedules import crontab
from api import api
from cache import cache
from flask import jsonify


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cache.init_app(app)

    db.init_app(app)

    mail.init_app(app)

    api.init_app(app)

    CORS(app, origins=['http://localhost:5173'], supports_credentials=True)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

    @app.template_filter('datetime')
    def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
        return value.strftime(format)

    with app.app_context():
        db.create_all()
        if not app.security.datastore.find_role("admin"):
            role = app.security.datastore.create_role(
                name="admin", description="Administrator"
            )
            db.session.commit()
        else:
            role = app.security.datastore.find_role("admin")

        if not app.security.datastore.find_user(email="admin@test.com"):
            user = app.security.datastore.create_user(
                first_name="Azhar",
                last_name="Bihari",
                email="admin@test.com",
                password=hash_password("password")
            )
            user.roles.append(role)
            db.session.commit()

    @app.route('/delete_table', methods=['GET'])
    def delete_table():
        db.session.execute(text('DELETE FROM booking'))
        db.session.commit()

    @app.route('/reset', methods=['GET'])
    def recreate_database():
        try:
            db.drop_all()
            db.create_all()
            return {'message': 'Database recreated successfully'}, 200
        except Exception as e:
            return {'message': 'Failed to recreate database', 'error': str(e)}, 500

    @app.route('/media/<path:filename>')
    def media(filename):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return send_from_directory(os.path.join(root_dir, 'media'), filename)

    @app.route('/download/<path:filename>', methods=['GET'])
    def download(filename):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return send_from_directory(os.path.join(root_dir), filename, as_attachment=True)

    celery = celery_init_app(app)
    celery.conf.enable_utc = False
    celery.conf.timezone = "Asia/Calcutta"
    celery.conf.beat_schedule = {
        'update-show-status': {
            'task': 'tasks.update_show_status',
            'schedule': crontab(minute='*'),
        },

        'update_dynamic_price': {
            'task': 'tasks.update_dynamic_price',
            'schedule': crontab(minute=0, hour='*/6'),
        },

        'send_inactive_user_email': {
            'task': 'tasks.send_inactive_user_email',
            'schedule': crontab(hour=18, minute=30),
        },

        'send_monthly_entertainment_report': {
            'task': 'tasks.send_monthly_entertainment_report',
            'schedule': crontab(hour=8, minute=0, day_of_month='1'),
        },

    }

    @app.before_request
    def perform_user_activity():
        if not current_user.is_authenticated:
            return

        endpoints = {'profile', 'mybookings', 'myreviews', 'home',
                     'show', 'city_shows', 'search', 'theater_shows'}

        endpoint = request.endpoint

        if endpoint in endpoints:
            show_id = request.view_args.get('show_id')
            theater_id = request.view_args.get('theater_id')
            add_user_activity.apply_async(
                args=(current_user.id, show_id or None, theater_id or None, request.path))

    return app, celery


app, celery = create_app()
