from datetime import timedelta
import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or "vGTcVLB3dP2juVX7gLaAeXcrbsjAHyB9"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'database.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = "GeZN8EDZaVefI4KY"
    SECURITY_TOKEN_MAX_AGE = 86400
    CACHE_TYPE = 'redis'

    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_OPTIONS = {
        'CACHE_REDIS_URL': CACHE_REDIS_URL,
        'CACHE_REDIS_PASSWORD': None,
    }

    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

    CELERY = {
        "broker_url": CELERY_BROKER_URL,
        "result_backend": CELERY_RESULT_BACKEND,
    }

    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '0a5ba10e521436'
    MAIL_PASSWORD = '547d4a7d41279c'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'noreply@ts.com'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "your_dev_secret_key"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'dev_database.db')
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '0a5ba10e521436'
    MAIL_PASSWORD = '547d4a7d41279c'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'noreply@dev.example.com'


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'prod_database.db')
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'your_prod_mail_username'
    MAIL_PASSWORD = 'your_prod_mail_password'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'noreply@example.com'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://prod_redis_server:6379/0'
    CACHE_OPTIONS = {
        'CACHE_REDIS_URL': CACHE_REDIS_URL,
        'CACHE_REDIS_PASSWORD': 'your_prod_redis_password',
    }
