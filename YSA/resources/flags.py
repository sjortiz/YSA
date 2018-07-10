from resources.db_client import DB


class Flags(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.flags

    def get(self, app):

        return {
            'data': [
                {
                    'uid': str(flag.get('_id', '')),
                    'name': flag.get('name', ''),
                }
                for flag in self.collection.find({"app": app})
            ]
        }
