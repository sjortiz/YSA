# Build-in libraries
from os import environ
from datetime import timedelta
# Third party/flask modules
from flask import Flask
from flask_restful import Api, reqparse, Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_refresh_token_required,
    get_jwt_identity, get_raw_jwt,
)
# Modules objects import
from resources.features import Features
from resources.apps import Apps
from resources.users import Users
from resources.tokens import Tokens

# Flask configs - adapters
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

# JWT configs
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY', 'default')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=2)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = environ.get(
    'JWT_REFRESH_EXPIRATION', False)
jwt = JWTManager(app)

# Module object initiaization
features = Features()
apps = Apps()
users = Users()
tokens = Tokens()

parser = reqparse.RequestParser()

parser.add_argument('user', type=str,  required=True,
                    help='Missing <<user>> parameter')
parser.add_argument('password', type=str,  required=True,
                    help='Missing <<password>> parameter')


@app.before_first_request
def set_default_user():
    users._set_default_user()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return tokens.token_blacklisted(decrypted_token)


class Login(Resource):
    """Returns a JWT access token.
    Clients must point here on initiation to request
    access to interact with the api.
    Only json request are accepted.
    """

    def post(self):

        args = parser.parse_args()
        return users.signin(**args)

    @jwt_refresh_token_required
    def put(self):
        return tokens._refresh_access_token(
            identity=get_jwt_identity()
        )


class SignUp(Resource):

    @jwt_required
    def post(self):

        args = parser.parse_args()
        return users.signup(**args)


class LogOut(Resource):

    @jwt_required
    def post(self):
        return tokens.blacklist_token(get_raw_jwt())

    @jwt_refresh_token_required
    def delete(self):
        return tokens.blacklist_token(get_raw_jwt())


class Apps(Resource):
    """Returns the list of apps, allows creation
    and deletion of apps.
    """

    def get(self, app=None):
        return apps.get(app)

    @jwt_required
    def post(self, app):
        return apps.post(app)

    @jwt_required
    def delete(self, app):
        return apps.delete(app)


class Features(Resource):
    """Returns the list of features"""

    def get(self, app=None, feature=None):
        # Returns all the features.
        # If the app is specified returns all the features in the app
        # If the feature is specified returns
        return features.get(app=app, feature=feature)


class FeatureMutations(Resource):
    """allows creation and deletion of features"""
    @jwt_required
    def post(self, app, feature):
        return features.post(app=app, feature=feature)

    @jwt_required
    def delete(self, app, feature):
        return features.delete(app=app, feature=feature)


class StatusMutation(Resource):
    """Allows mutation of status"""
    @jwt_required
    def put(self, app, feature):
        return features.put(app=app, feature=feature)


class HealthCheck(Resource):
    """Just to see if the app is running"""

    def get(self):
        return {'status': 'ok'}, 200


# healt-check routes
api.add_resource(HealthCheck, '/', '/healthcheck')
# login route
api.add_resource(Login, '/login')
# sign up
api.add_resource(SignUp, '/signup')
# log out
api.add_resource(LogOut, '/logout')
# apps entity routes
api.add_resource(Apps, '/apps', '/apps/<app>')
# features entity routes
api.add_resource(Features, '/features', '/features/<app>',
                 '/features/<app>/<feature>')
api.add_resource(FeatureMutations, '/feature/<app>/<feature>')
api.add_resource(StatusMutation, '/status/<app>/<feature>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8080")
