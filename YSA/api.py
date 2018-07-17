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
from resources.groups import Groups
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
groups = Groups()
# Arguments parsing
parser = reqparse.RequestParser()

parser.add_argument('user', type=str,  required=True,
                    help='Missing <<user>> parameter')
parser.add_argument('password', type=str,  required=True,
                    help='Missing <<password>> parameter')


@app.before_first_request
def set_default_user():
    # Creates a default user if there is not any user
    users._set_default_user()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    # Cerify if the token is not black-listed
    return tokens.token_blacklisted(decrypted_token)


class Login(Resource):
    """Returns a JWT access token.
    Clients must point here on initiation to request
    access to interact with the api.
    Only json request are accepted.
    """

    def post(self):
        # Returns user tokens if loged or error if fails
        args = parser.parse_args()
        return users.signin(**args)

    @jwt_refresh_token_required
    def put(self):
        # Refresh jwt token specs jwt_refresh token
        return tokens._refresh_access_token(
            identity=get_jwt_identity()
        )


class SignUp(Resource):
    """Register an user."""
    @jwt_required
    def post(self):
        # Creates an user
        args = parser.parse_args()
        return users.signup(**args)


class LogOut(Resource):
    """Blacklist the tokens, you must hit it with both methods
    to enable the full secuirty, if you just want to destroy
    a missed token hit the corresponding one.
    """
    @jwt_required
    def post(self):
        return tokens.blacklist_token(get_raw_jwt())

    @jwt_refresh_token_required
    def delete(self):
        return tokens.blacklist_token(get_raw_jwt())


class Apps(Resource):
    """Returns the list of apps."""

    def get(self, app=None):
        # Returns all the apps or the app specified
        return apps.get(app)


class AppMutations(Resource):
    """Allows creation and deletion of apps."""
    @jwt_required
    def post(self, app):
        # Creates a new app
        return apps.post(app)

    @jwt_required
    def delete(self, app):
        # Deletes an app
        return apps.delete(app)


class Groups(Resource):
    """Returns the list of groups"""

    def get(self, app=None, group=None):
        return groups.get(app=app, group=group)


class GroupMutation(Resource):
    """Allows creation and deletion of apps"""
    @jwt_required
    def post(self, app, group):
        return groups.post(app=app, group=group)

    @jwt_required
    def delete(self, app, group):
        return groups.delete(app=app, group=group)


class Features(Resource):
    """Returns the list of features."""

    def get(self, group=None, feature=None):
        # Returns all the features.
        # If the app is specified returns all the features in the app
        # If the feature is specified returns
        return features.get(group=group, feature=feature)


class FeatureMutations(Resource):
    """allows creation and deletion of features"""
    @jwt_required
    def post(self, group, feature):
        # Creates a feature
        return features.post(group=group, feature=feature)

    @jwt_required
    def delete(self, group, feature):
        # Deletes a feature
        return features.delete(group=group, feature=feature)


class StatusMutation(Resource):
    """Allows mutation of feature status"""
    @jwt_required
    def put(self, group, feature):
        # Toggles the feature status
        return features.put(group=group, feature=feature)


class HealthCheck(Resource):
    """Confirms if the app is running"""

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
api.add_resource(Apps, '/apps')
api.add_resource(AppMutations, '/app/<app>')
# groups entity routes
api.add_resource(Groups, '/groups', '/groups/<app>')
api.add_resource(GroupMutation, '/group/<app>/<group>')
# features entity routes
api.add_resource(Features, '/features', '/features/<group>',
                 '/features/<group>/<feature>')
api.add_resource(FeatureMutations, '/feature/<group>/<feature>')
# feature status routes
api.add_resource(StatusMutation, '/status/<group>/<feature>')


if __name__ == '__main__':

    app.run(
        debug=environ.get('FFAAS_DEBUG', False),
        host='0.0.0.0',
        port="8080",
    )
