from pymongo import ReturnDocument
from resources.db_client import DB
from resources.apps import Apps

apps = Apps()


class Features(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.features

    def get(self, app=None, feature=None):

        limiter = {}

        if app:
            limiter.update({'app': app})

        if feature:
            limiter.update({'feature': feature})

        return {
            'data': [
                {
                    'id': str(feature.get('_id', '')),
                    'app': feature.get('app', ''),
                    'feature': feature.get('feature', ''),
                    'status': feature.get('status', False),
                }
                for feature in self.collection.find(limiter)
            ]
        }

    def post(self, app, feature):

        data = self.get(app, feature)

        if data.get('data', False):
            return {
                'errors': [
                    {
                        'status': '409',
                        'source': {'pointer': f'/features/{app}/{feature}'},
                        'title': 'Duplicated feature record',
                        'details': f'The feature {feature} already exist'
                    }

                ]
            }, 409

        if apps.get(app).get('data', False):

            _id = self.collection.insert_one(
                {
                    'app': app,
                    'feature': feature,
                }
            ).inserted_id

            return {
                'data': [

                    {
                        'id': str(_id),
                        'app': app,
                        'feature': feature,
                        'status': False,
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

    def put(self, app, feature):

        _filter = {
            'app': app,
            'feature': feature,
        }

        data = self.get(app, feature).get('data')

        if not data:

            return {
                'errors': [
                    {
                        'status': '409',
                        'source': {'pointer': f'/features/{feature}'},
                        'title':  'Feature entry not found',
                        'details': (
                            f'The feature {feature}'
                            f' is not registrered for the app <<{app}>>'
                        )
                    }
                ]
            }, 409

        status = not bool(data[0].get('status', False))

        updater = {'$set': {
            'status': status
        }}

        result = self.collection.find_one_and_update(
            _filter,
            updater,
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        del result['_id']

        return {
            'data': [

                {
                    **result,
                }
            ]
        }, 200

    def delete(self, app, feature):

        result = self.collection.remove({
            'app': app,
            'feature': feature,
        })

        deleted = result['n']

        return {
            'data': [
                {
                    'feature': feature,
                    'deleted': deleted,
                }
            ]
        }
