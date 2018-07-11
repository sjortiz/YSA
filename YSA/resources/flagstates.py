from pymongo import ReturnDocument
from resources.db_client import DB
from resources.features import Features

features = Features()


class FlagStates(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.flags

    def get(self, app, feature):

        doc = self.collection.find_one({
            'app': app,
            'feature': feature,
        })

        result = {
            'data': []
        }

        if doc:

            del doc['_id']

            result['data'].append(doc)

        return result

    def post(self, app, feature):

        _filter = {
            'app': app,
            'feature': feature,
        }

        data = self.get(app, feature).get('data')

        if not (data or features.get(feature).get('data')):

            return {
                'errors': [
                    {
                        'status': '404',
                        'source': {'pointer': f'/features/{feature}'},
                        'title':  'Feature entry not found',
                        'details': (
                            f'The feature {feature}'
                            ' was is not registrered'
                        )
                    }
                ]
            }, 404

        status = not (bool(data) and data[0].get('status', False))

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
            # response, status
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
                    'app': app,
                    'feature': feature,
                    'deleted': deleted,
                }
            ]
        }
