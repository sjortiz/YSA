from resources.db_client import DB
from resources.tokens import Tokens


class Apps(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.apps

    def get(self, name: str='') -> tuple:
        # Get a list of all the apps and it's information
        # Gets the app information if the name is specified
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
        }, 200

    def post(self, app: str) -> tuple:

        if self.collection.find_one({'name': app}):

            return {
                'errors': [
                    {
                        'status': '409',
                        'source': {'pointer': f'/app/{app}'},
                        'title': 'Duplicated app record',
                        'details': f'The app {app} already exist'
                    }

                ]
            }, 409

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
        }, 200

    def delete(self, app: str) -> tuple:

        result = self.collection.remove({"name": app})
        deleted = result['n']

        return {
            'data': [
                {
                    'name': app,
                    'deleted': deleted,
                }
            ]
        }, 200
