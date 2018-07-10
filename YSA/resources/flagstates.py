from resources.db_client import DB
from pymongo import ReturnDocument


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

        if data:
            status = not bool(data[0].get('status', False))

        else:
            status = True

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
        }

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
