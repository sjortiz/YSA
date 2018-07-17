from pymongo import ReturnDocument
from resources.db_client import DB
from resources.groups import Groups

groups = Groups()


class Features(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.features

    def get(self, group: str='', feature: str='') -> tuple:

        limiter = {}

        if group:
            limiter.update({'group': group})

        if feature:
            limiter.update({'feature': feature})

        return {
            'data': [
                {
                    'id': str(feature.get('_id', '')),
                    'group': feature.get('group', ''),
                    'feature': feature.get('feature', ''),
                    'status': feature.get('status', False),
                }
                for feature in self.collection.find(limiter)
            ]
        }, 200

    def post(self, group: str, feature: str) -> tuple:

        data = self.get(group, feature)[0]

        if data.get('data', False):
            return {
                'errors': [
                    {
                        'status': '409',
                        'source': {'pointer': f'/features/{group}/{feature}'},
                        'title': 'Duplicated feature record',
                        'details': f'The feature {feature} already exist'
                    }

                ]
            }, 409

        if groups.get(group=group)[0].get('data', False):

            _id = self.collection.insert_one(
                {
                    'group': group,
                    'feature': feature,
                }
            ).inserted_id

            return {
                'data': [

                    {
                        'id': str(_id),
                        'group': group,
                        'feature': feature,
                        'status': False,
                    }
                ]
            }, 200

        return {
            'errors': [
                {
                    'status': '409',
                    'source': {'pointer': f'/groups/{group}'},
                    'title':  'group entry not found',
                    'details': (
                        f'The group {group} is not registrered'
                    )
                }
            ]
        }, 409

    def put(self, group: str, feature: str) -> tuple:

        _filter = {
            'group': group,
            'feature': feature,
        }

        data = self.get(group, feature)[0].get('data')

        if not data:

            return {
                'errors': [
                    {
                        'status': '409',
                        'source': {'pointer': f'/features/{feature}'},
                        'title':  'Feature entry not found',
                        'details': (
                            f'The feature {feature}'
                            f' is not registrered for the group <<{group}>>'
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

    def delete(self, group: str, feature: str) -> tuple:

        result = self.collection.remove({
            'group': group,
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
        }, 200
