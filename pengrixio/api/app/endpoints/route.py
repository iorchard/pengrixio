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
from guacamole.client import GuacamoleClient

from pengrixio.api.restplus import api

from pengrixio.api.app.serializers import appSerializer
from pengrixio.api.app.serializers import appPostSerializer

from pengrixio.api.app.bizlogic import get_app
from pengrixio.api.app.bizlogic import create_app
from pengrixio.api.app.bizlogic import delete_app
from pengrixio.api.app import client

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

@ns.route('/connect/<string:name>/')
@api.response(404, 'App not found.')
class AppConnect(Resource):

    def get(self, name):
        """Returns the app connect information."""
        response = make_response(render_template('connect.html', name=name))
        response.headers.set("Content-Type", "text/html")
        return response

@ns.route('/tunnel/<string:name>/<int:width>/<int:height>/')
@api.response(404, 'App not found.')
class AppTunnel(Resource):

    def get(self, name, width, height):
        d = request.args
        k = [k for k, v in d.items()][0]
        tokens = k.split(':')
        if len(tokens) >=2:
            return _do_read(request, tokens[1])

        return Response(status=400)

    def post(self, name, width, height):
        d = request.args
        k = [k for k, v in d.items()][0]
        if k == 'connect':
            return _do_connect(request, name, width, height)
        else:
            tokens = k.split(':')
            if len(tokens) >=2:
                return _do_write(request, tokens[1])

        return Response(status=400)

def _do_connect(request, name, width, height):
    # Get the node internal ip on which VM is running.
    s_node_ip = '192.168.10.10'
    # Connect to guacd daemon
    guac = client.GuacamoleClient(host=s_node_ip, port=4822, timeout=10)

    s_vm_ip = '192.168.10.22'
    log.debug("{} {}x{}".format(s_vm_ip, width, height))
    s_vm_username = 'orchard'
    s_vm_password = 'i0rchard'
    s_client_name = "{} RDP Client".format(name)
    guac.connect(protocol='rdp',
                 hostname=s_vm_ip,
                 port=31422,
                 username=s_vm_username,
                 password=s_vm_password,
                 console='false',
                 server_layout='ko-kr-qwerty', # 'failsafe','en-us-qwerty',
                 color_depth=24,
                 width=width,
                 height=height,
                 enable_wallpaper='false',
                 enable_theming='true',
                 enable_font_smoothing='true',
                 client_name=s_client_name,
                 disable_audio='false',
                 enable_drive='false'
    )

    cache_key = str(uuid.uuid4())
    with sockets_lock:
        log.info('Saving socket with key{} val {}'.format(cache_key, guac))
        sockets[cache_key] = guac
    response = Response(response=cache_key)
    #response['Cache-Control'] = 'no-cache'

    return response

def _do_read(request, cache_key):
    pending_read_request.set()

    def content():
        with sockets_lock:
            guac = sockets[cache_key]

        with read_lock:
            pending_read_request.clear()

            while True:
                content = guac.read()
                if content:
                    yield content
                else:
                    break

                if pending_read_request.is_set():
                    # log.info('Letting another request take over.')
                    break

            # End-of-instruction marker
            yield '0.;'

    response = Response(content(), content_type='application/octet-stream')
    #response['Cache-Control'] = 'no-cache'
    return response


def _do_write(request, cache_key):
    with sockets_lock:
        guac = sockets[cache_key]

    with write_lock:
        while True:
            chunk = request.stream.read(8192)
            if chunk:
                guac.write(chunk)
            else:
                break

    response = Response(content_type='application/octet-stream')
    #response['Cache-Control'] = 'no-cache'
    return response
