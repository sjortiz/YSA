from flask import request
from resources.db_client import DB
from resources.tokens import Tokens


class Users(DB):

    def __init__(self):

        super().__init__()
        self.collection = self.db.users

    def __query_user(self, user: str=None) -> dict:
        # Looks for an user in the db
        return self.collection.find_one(
            {'user': user} if user else {}
        )

    def __validate_credentials(self, user: str, password: str) -> tuple:
        # Ensure that the credentials provided match the ones in user the table
        user_data = self.__query_user(user=user)

        if user_data:

            if password == user_data.get('password'):
                return Tokens.generate_token_pair(user), 200

            return {
                'errors': [
                    {
                        'status': '401',
                        'source': {'pointer': '/login'},
                        'title':  'Unauthorized',
                        'details': f'Wrong password specified'
                    }
                ]
            }, 401

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

    def signin(self, user: str, password: str)->tuple:
        # Attempts to log the user in
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

    def signup(self, user: str, password: str) -> tuple:
        # Creates an user
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

    def _set_default_user(
            self, user: str='admin', password: str='admin') -> None:
        # Adds the default user if the user document is empty
        if not self.__query_user():
            self.signup(user, password)
