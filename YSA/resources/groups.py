from resources.db_client import DB
from resources.apps import Apps

apps = Apps()


class Groups(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.groups

    def get(self, app: str='', group: str='') -> tuple:

        limiter = {}

        if app:
            limiter.update({'app': app})

        if group:
            limiter.update({'group': group})

        return {
            'data': [
                {
                    'id': str(group.get('_id', '')),
                    'app': group.get('app', ''),
                    'group': group.get('group', ''),
                    'status': group.get('status', False),
                }
                for group in self.collection.find(limiter)
            ]
        }, 200

    def post(self, app: str, group: str) -> tuple:

        data = self.get(app, group)

        if data.get('data', False):
            return {
                'errors': [
                    {
                        'status': '409',
                        'source': {'pointer': f'/groups/{app}/{group}'},
                        'title': 'Duplicated group record',
                        'details': f'The group {group} already exist'
                    }

                ]
            }, 409

        if apps.get(app).get('data', False):

            _id = self.collection.insert_one(
                {
                    'app': app,
                    'group': group,
                }
            ).inserted_id

            return {
                'data': [

                    {
                        'id': str(_id),
                        'app': app,
                        'group': group,
                        'status': False,
                    }
                ]
            }, 200

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

    def delete(self, app: str, group: str) -> tuple:

        result = self.collection.remove({
            'app': app,
            'group': group,
        })

        deleted = result['n']

        return {
            'data': [
                {
                    'group': group,
                    'deleted': deleted,
                }
            ]
        }, 200
