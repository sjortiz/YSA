from resources.db_client import DB
from resources.tokens import Tokens


class Apps(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.apps

    def get(self, name=None):

        return {
            'data': [
                {
                    'id': str(app.get('_id', '')),
                    'name': app.get('name', ''),
                }
                for app in self.collection.find(
                    {'name': name} if name else {}
                )
            ]
        }

    def post(self, app):

        data = {
            'name': app,
            'tokens': Tokens.generate_token_pair(app),
        }

        self.collection.insert_one(data)

        del data['_id']

        return {
            'data': [

                {
                    **data,
                }
            ]
        }

    def delete(self, app):

        result = self.collection.remove({"name": app})
        deleted = result['n']

        return {
            'data': [
                {
                    'name': app,
                    'deleted': deleted,
                }
            ]
        }
