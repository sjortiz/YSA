from resources.db_client import DB


class Tokens(DB):

    def __init__(self):

        super().__init__()
        self.collection = self.db.tokens

    def token_blacklisted(self, raw_token):
        if self.collection.find_one({
            'token': raw_token['jti'],
            'status': 'revoked',
        }):
            return True

        return False

    def blacklist_token(self, raw_token):

        self.collection.insert_one({
            'token': raw_token['jti'],
            'status': 'revoked',
        })

        return {
            'data': [
                {'message': 'ok'}
            ]
        }, 200
