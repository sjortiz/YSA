from resources.db_client import DB
from resources.apps import Apps

apps = Apps()


class Features(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.features

    def get(self, name, app=None):

        limiter = {}

        if name:
            limiter.update({'name': name})

        if app:
            limiter.update({'app': app})

        return {
            'data': [
                {
                    'id': str(feature.get('_id', '')),
                    'app': feature.get('app', ''),
                    'name': feature.get('name', ''),
                }
                for feature in self.collection.find(limiter)
            ]
        }

    def post(self, feature, app):

        data = self.get(feature, app)

        if data.get('data', False):
            return data

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
                        'app': app,
                        'name': feature,
                    }
                ]
            }

        return {
            'errors': [
                {
                    'status': '409',
                    'source': {'pointer': f'/apps/{app}'},
                    'title':  'App entry not found',
                    'details': (
                        f'The app {app} is not registrered'
                    )
                }
            ]
        }, 409

    def delete(self, feature, app):

        result = self.collection.remove({
            'name': feature,
            'app': app,
        })

        deleted = result['n']

        return {
            'data': [
                {
                    'name': feature,
                    'deleted': deleted,
                }
            ]
        }
