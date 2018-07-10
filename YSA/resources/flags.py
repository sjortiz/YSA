from resources.db_client import DB


class Flags(DB):

    def __init__(self):
        super().__init__()

        self.collection = self.db.flags

    def get(self, app):

        return {
            'data': [
                {
                    'app': flag.get('app'),
                    'feature': flag.get('feature'),
                    'status': flag.get('status')
                }
                for flag in self.collection.find({'app': app} if app else None)
            ]
        }
