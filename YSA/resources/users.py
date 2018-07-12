from flask import request
from flask_jwt_extended import (
    create_access_token, create_refresh_token)
from resources.db_client import DB


class Users(DB):

    def __init__(self):

        super().__init__()
        self.collection = self.db.users

    def __query_user(self, user=None):
        return self.collection.find_one(
            {'user': user} if user else {}
        )

    @staticmethod
    def __generate_access_token(identity):
        return create_access_token(identity=identity)

    @staticmethod
    def __generate_refresh_token(identity):
        return create_refresh_token(identity=identity)

    @classmethod
    def _refresh_access_token(cls, identity):
        return {
            'access_token': cls.__generate_access_token(identity)
        }, 200

    def __validate_credentials(self, user, password):

        user_data = self.__query_user(user=user)

        if user_data:

            if password == user_data.get('password'):
                return {
                    'access_token': self.__generate_access_token(user),
                    'refresh_token': self.__generate_refresh_token(user)
                }, 200

            return ({
                'errors': [
                    {
                        'status': '401',
                        'source': {'pointer': '/login'},
                        'title':  'Unauthorized',
                        'details': f'Wrong password specified'
                    }
                ]
            }, 401)

        return {
            'errors': [
                {
                    'status': '404',
                    'source': {'pointer': '/login'},
                    'title': 'User not found',
                    'details': f'The user <<{user}>> was not found',
                }
            ]
        }, 404

    def signin(self, user, password):

        if not request.is_json:

            return {
                "errors": [
                    {
                        'status': '415',
                        'source': {'pointer': '/login'},
                        'title':  'Unsupported media type',
                        'detail': 'This endpoints only supports json requests',
                    }
                ]
            }, 415

        data = request.get_json()

        if 'user' in data and 'password' in data:
            return self.__validate_credentials(**data)

        return {
            "errors": [
                {
                    'status': '422',
                    'source': {'pointer': '/login'},
                    'title':  'Unprocessable Entity',
                    'detail': 'The accepted parameters are user and password',
                }
            ]
        }, 422

    def signup(self, user, password):

        data = {
            'user': user,
            'password': password,
        }

        self.collection.insert_one(data)

        return {
            'data': [
                {
                    'id': str(data['_id']),
                    'user': data['user'],
                }
            ]
        }, 200

    def _set_default_user(self, user='admin', password='admin'):
        if not self.__query_user():
            self.signup(user, password)
