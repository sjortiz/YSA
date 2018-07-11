from resources.db_client import DB


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

        _id = self.collection.insert_one(
            {
                'name': app
            }
        ).inserted_id

        return {
            'data': [

                {
                    'id': str(_id),
                    'name': app,
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
