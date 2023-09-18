from flask import abort
from flask_restful import Resource, marshal_with, reqparse
from flask_security import auth_required, current_user, SQLAlchemyUserDatastore, hash_password, verify_password, logout_user
from api.marshals import user_marshal
from api.parsers import login_parser, register_parser
from models import User, db, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class UserResource(Resource):
    @auth_required()
    @marshal_with(user_marshal)
    def get(self):
        try:
            user = current_user
            if not user:
                abort(404, message='User not found')
            return user, 200
        except Exception as e:
            abort(500, message='Internal Server Error', error=str(e))


class RegisterResource(Resource):
    def post(self):
        try:
            args = register_parser.parse_args()
            if not all(args.values()):
                abort(400, message='All fields are required')

            if user_datastore.find_user(email=args['email']):
                abort(409, message='User with this email already exists')

            args['password'] = hash_password(args['password'])
            user = user_datastore.create_user(**args)
            db.session.commit()
            auth_token = user.get_auth_token()
            return {'message': 'User registered successfully', 'auth_token': auth_token}, 201
        except Exception as e:
            abort(500, message='Internal Server Error', error=str(e))


class LoginResource(Resource):
    def post(self):
        try:
            args = login_parser.parse_args()
            if not all(args.values()):
                abort(400, message='All fields are required')

            user = user_datastore.find_user(email=args['email'])
            if not user or not verify_password(args['password'], user.password):
                abort(401, message='Invalid credentials')

            auth_token = user.get_auth_token()
            return {'auth_token': auth_token}, 200
        except Exception as e:
            abort(500, message='Internal Server Error', error=str(e))


class LogoutResource(Resource):
    @auth_required()
    def post(self):
        try:
            logout_user()
            return {'message': 'Logged out successfully'}, 200
        except Exception as e:
            abort(500, message='Internal Server Error', error=str(e))
