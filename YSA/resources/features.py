from resources.db_client import DB
from resources.apps import Apps

apps = Apps()


class Features(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.features

    def get(self, name):

        return {
            'data': [
                {
                    'uid': str(feature.get('_id', '')),
                    'name': feature.get('name', ''),
                }
                for feature in self.collection.find(
                    {'name': name} if name else {}
                )
            ]
        }

    def post(self, feature, app):

        if apps.get(app).get('data', False):

            _id = self.collection.insert_one(
                {
                    'app': app,
                    'name': feature,
                }
            ).inserted_id

            return {
                'data': [

                    {
                        'id': str(_id),
                        'name': feature,
                    }
                ]
            }

        return {
            'errors': [
                {
                    'status': '404',
                    'source': {'pointer': f'/apps/{app}'},
                    'title':  'App entry not found',
                    'details': (
                        f'The app {app} was is not registrered'
                    )
                }
            ]
        }, 404

    def delete(self, feature):

        result = self.collection.remove({"name": feature})
        deleted = result['n']

        return {
            'data': [
                {
                    'name': feature,
                    'deleted': deleted,
                }
            ]
        }
