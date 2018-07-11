from flask import Flask
from flask_restful import Resource, Api
from resources.features import Features
from resources.apps import Apps
from resources.flags import Flags
from resources.flagstates import FlagStates

app = Flask(__name__)
api = Api(app)
features = Features()
apps = Apps()
flags = Flags()
flagstates = FlagStates()


class Apps(Resource):
    """Returns the list of apps, allows creation
    and deletion of apps.
    """

    def get(self, app=None):
        return apps.get(app)

    def post(self, app):
        return apps.post(app)

    def delete(self, app):
        return apps.delete(app)


class Features(Resource):
    """Returns the list of features, allows creation
    and deletion of features.
    """

    def get(self, feature=None):
        return features.get(feature)

    def post(self, feature, app):
        return features.post(feature, app)

    def delete(self, feature, app):
        return features.delete(feature)


class Flags(Resource):
    """Returns all the flags. If the app is specified
    returns all the flags by app.
    """

    def get(self, app=None):
        return flags.get(app)


class FlagStates(Resource):
    """Returns the status of a flag in an app, allows
    modification thru the post method of the flag status.
    Creates the association if it doesn't exist yet.
    """

    def get(self, app, feature):
        return flagstates.get(app, feature)

    def post(self, app, feature):
        return flagstates.post(app, feature)

    def delete(self, app, feature):
        return flagstates.delete(app, feature)


class HealthCheck(Resource):
    """Just to see if the app is running"""

    def get(self):
        return {'status': 'ok'}, 200


# apps entity routes
api.add_resource(Apps, '/apps', '/apps/<app>')
# features entity routes
api.add_resource(Features, '/features', '/features/<feature>',
                 '/features/<feature>/<app>')
# flags entity routes
api.add_resource(Flags, '/flags', '/flags/<app>')
api.add_resource(FlagStates, '/flags/status/<app>/<feature>')
# healt-check routes
api.add_resource(HealthCheck, '/', '/healthcheck')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8080")
