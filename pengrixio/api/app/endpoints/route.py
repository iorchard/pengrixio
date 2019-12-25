import logging
import logging.config
import uuid
import threading
import time

from flask import request
from flask import abort
from flask import render_template
from flask import make_response
from flask import Response
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from pengrixio.api.restplus import api

from pengrixio.api.app.serializers import appSerializer
from pengrixio.api.app.serializers import appPostSerializer

from pengrixio.api.app.bizlogic import get_app
from pengrixio.api.app.bizlogic import create_app
from pengrixio.api.app.bizlogic import delete_app
from pengrixio.api.app.bizlogic import connect_app
from pengrixio.api.app.bizlogic import operate_app

sockets = {}
sockets_lock = threading.RLock()
read_lock = threading.RLock()
write_lock = threading.RLock()
pending_read_request = threading.Event()

log = logging.getLogger('pengrixio')

ns = api.namespace('app', description="Operations for app")

@ns.route('/')
class AppCollection(Resource):

    @api.marshal_list_with(appSerializer)
    @jwt_required
    def get(self):
        """Returns list of app."""
        l_app = get_app()
        return l_app

    @api.response(201, 'App successfully created.')
    @api.expect(appPostSerializer)
    @jwt_required
    def post(self):
        """Creates a new app.
        """
        data = request.json
        log.debug(data)
        (b_ret, s_msg) = create_app(data)
        if not b_ret:
            d_msg = {'error': 'App creation is failed.'}
            return d_msg, 400

        # Get a newly created app info.
        #l_app = get_app(data['name'])

        return {}, 201

@ns.route('/<string:name>/')
@api.response(404, 'App not found.')
class AppItem(Resource):

    @api.marshal_with(appSerializer)
    @api.doc('get_something')
    @jwt_required
    def get(self, name):
        """Returns the app information."""
        l_app = get_app(name)
        if not len(l_app):
            d_msg = {'error': 'name {} is not found.'.format(name)}
            return d_msg, 404

        return l_app[0]

    @api.response(204, "The app is successfully deleted.")
    @jwt_required
    def delete(self, name):
        """Deletes the app."""
        (b_ret, s_msg) = delete_app(name)
        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 404

        return None, 204

@ns.route('/user/:<string:user>/')
@api.response(404, 'App not found.')
class AppUser(Resource):

    @api.marshal_with(appSerializer)
    @jwt_required
    def get(self, user):
        """Returns the app information."""
        l_app = get_app(None, user)

        return l_app

@ns.route('/<string:name>/connect/')
@api.response(404, 'App not found.')
class AppConnect(Resource):

    #@jwt_required
    def get(self, name):
        """Returns the app broker information."""
        (b_ret, s_broker) = connect_app(name)
        if not b_ret:
            return s_broker, 404

        return s_broker

@ns.route('/<string:name>/<string:action>/')
class AppAction(Resource):

    @api.response(201, 'App runs successfully.')
    @jwt_required
    def post(self, name, action):
        """Run/Stop an app.
        """
        (b_ret, s_msg) = operate_app(name, action)

        if not b_ret:
            d_msg = {'error': s_msg}
            return d_msg, 400

        return {}, 201
