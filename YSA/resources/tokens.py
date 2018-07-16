from resources.db_client import DB
from flask_jwt_extended import (
    create_access_token, create_refresh_token)


class Tokens(DB):
    def __init__(self):

        super().__init__()
        self.collection = self.db.tokens

    @staticmethod
    def __generate_access_token(identity: str) -> dict:
        # Generates access token based on identity
        return create_access_token(identity=identity)

    @staticmethod
    def __generate_refresh_token(identity: str) -> dict:
        # Generates refresh token based on identity
        return create_refresh_token(identity=identity)

    @classmethod
    def _refresh_access_token(cls, identity: str) -> tuple:
        # Refresh access token based on identity
        return {
            'access_token': cls.__generate_access_token(identity)
        }, 200

    @classmethod
    def generate_token_pair(cls, identity: str) -> dict:
        # Generates access and refresh token
        return {
            'access_token': cls.__generate_access_token(identity),
            'refresh_token': cls.__generate_refresh_token(identity)
        }

    def token_blacklisted(self, raw_token: str) -> bool:
        # Checks if token was blacklisted
        if self.collection.find_one({
            'token': raw_token['jti'],
            'status': 'revoked',
        }):
            return True

        return False

    def blacklist_token(self, raw_token: str) -> tuple:
        # Adds the token to the blacklist
        self.collection.insert_one({
            'token': raw_token['jti'],
            'status': 'revoked',
        })

        return {
            'data': [
                {'message': 'ok'}
            ]
        }, 200
