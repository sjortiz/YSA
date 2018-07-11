from resources.db_client import DB


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

    def post(self, feature):

        _id = self.collection.insert_one(
            {
                'name': feature
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
